import os
import json
import math
import argparse
import joblib
import numpy as np
import pandas as pd
import xgboost as xgb
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import RandomizedSearchCV, TimeSeriesSplit
from sklearn.metrics import classification_report, accuracy_score, log_loss
from sklearn.calibration import CalibratedClassifierCV
from sklearn.base import clone

RUTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(RUTA)
os.makedirs('Predicciones', exist_ok=True)

np.random.seed(42)

# ====================================================================
# PARÁMETROS GLOBALES
# ====================================================================

N_SIMULACIONES = 10_000
T_GRUPOS       = 1.0
T_CRUCES       = 1.0
T_FORZADA      = 1
DECAY_RECENCIA = 0.0005
FORZAR_REENTRENAMIENTO = False
N_ITER_REG = 300
N_ITER_1X2 = 500
tweedie_parameter = 1.2
CV_SPLITS = 5
CPU_THREADS = max(1, os.cpu_count() or 1)
CALIBRATION_METHOD = 'isotonic'
RUTA_RESULTADOS_REALES = './Data/resultados_reales.csv'
ANFITRIONES_2026 = {'EE. UU.', 'México', 'Canadá'}
FACTOR_GOL_DINAMICO = 1.0
FACTOR_GOL_MIN = 0.85
FACTOR_GOL_MAX = 1.35


def configurar_perfil(nombre):
    """Ajusta el coste de entrenamiento sin cambiar el pipeline."""
    global N_SIMULACIONES, N_ITER_REG, N_ITER_1X2
    global CV_SPLITS, CPU_THREADS, CALIBRATION_METHOD

    perfiles = {
        'full': dict(sims=10_000, reg=300, clf=500, cv=5,
                     threads=max(1, os.cpu_count() or 1), calibration='isotonic'),
        'colab': dict(sims=5_000, reg=16, clf=24, cv=3,
                      threads=2, calibration='sigmoid'),
        'test': dict(sims=100, reg=1, clf=1, cv=2,
                     threads=1, calibration='sigmoid'),
    }
    cfg = perfiles[nombre]
    N_SIMULACIONES = cfg['sims']
    N_ITER_REG = cfg['reg']
    N_ITER_1X2 = cfg['clf']
    CV_SPLITS = cfg['cv']
    CPU_THREADS = min(cfg['threads'], max(1, os.cpu_count() or 1))
    CALIBRATION_METHOD = cfg['calibration']

# ====================================================================
# GRIDS DE HIPERPARÁMETROS
# ====================================================================

PARAM_GRID_REG = {
    'n_estimators':     [100, 200, 300, 500],
    'learning_rate':    [0.005, 0.01, 0.05, 0.1, 0.2, 0.5],
    'max_depth':        [2, 3, 5, 8],
    'subsample':        [0.8, 0.9, 1.0],
    'reg_lambda':       [0.1, 0.5, 1.0, 5.0],
    'gamma':            [0, 0.1],
    'colsample_bytree': [0.8, 0.9, 1.0],
}

PARAM_GRID_1X2 = {
    'n_estimators':     [100, 200, 300, 500, 700, 1000],
    'learning_rate':    [0.005, 0.01, 0.02, 0.05, 0.1, 0.2],
    'max_depth':        [2, 3, 4, 5],
    'subsample':        [0.7, 0.8, 0.9, 1.0],
    'reg_lambda':       [0.1, 0.5, 1.0, 2.0, 5.0],
    'reg_alpha':        [0, 0.1, 0.5, 1.0],
    'gamma':            [0, 0.05, 0.1, 0.2],
    'colsample_bytree': [0.7, 0.8, 0.9, 1.0],
    'min_child_weight': [1, 3, 5],
}

# ====================================================================
# FUNCIONES AUXILIARES
# ====================================================================

def asignar_tier(puntos):
    if puntos >= 1700: return 1
    elif puntos >= 1600: return 2
    elif puntos >= 1500: return 3
    else: return 4

mapa_continentes = {
    'República Checa': 'Europa', 'Bosnia-Herzegovina': 'Europa', 'Suiza': 'Europa',
    'Países Bajos': 'Europa', 'Alemania': 'Europa', 'Escocia': 'Europa',
    'Turquía': 'Europa', 'Suecia': 'Europa', 'España': 'Europa',
    'Bélgica': 'Europa', 'Francia': 'Europa', 'Croacia': 'Europa',
    'Austria': 'Europa', 'Portugal': 'Europa', 'Inglaterra': 'Europa',
    'Noruega': 'Europa',
    'Paraguay': 'Sudamérica', 'Brasil': 'Sudamérica', 'Ecuador': 'Sudamérica',
    'Uruguay': 'Sudamérica', 'Argentina': 'Sudamérica', 'Colombia': 'Sudamérica',
    'México': 'Norteamérica', 'Canadá': 'Norteamérica', 'EE. UU.': 'Norteamérica',
    'Haití': 'Norteamérica', 'Curazao': 'Norteamérica', 'Panamá': 'Norteamérica',
    'Sudáfrica': 'Africa', 'Marruecos': 'Africa', 'Egipto': 'Africa',
    'Túnez': 'Africa', 'Costa de Marfil': 'Africa', 'Cabo Verde': 'Africa',
    'Senegal': 'Africa', 'RD Congo': 'Africa', 'Argelia': 'Africa',
    'Ghana': 'Africa',
    'Corea del Sur': 'Asia', 'Catar': 'Asia', 'Japón': 'Asia',
    'Australia': 'Asia', 'Irán': 'Asia', 'Arabia Saudí': 'Asia',
    'Jordania': 'Asia', 'Irak': 'Asia', 'Uzbekistán': 'Asia',
    'Nueva Zelanda': 'Asia',
}

pesos_continente = {
    'Europa': 1.00, 'Sudamérica': 0.95, 'Norteamérica': 0.75,
    'Africa': 0.6, 'Asia': 0.7, 'Oceanía': 0.5,
}


def tunear_temperatura(probs, y_true, name="General"):
    best_t, best_loss = 1.0, float('inf')
    for t in np.arange(0.1, 3.1, 0.01):
        p_t = probs ** (1 / t)
        p_t = p_t / p_t.sum(axis=1, keepdims=True)
        loss = log_loss(y_true, p_t)
        if loss < best_loss:
            best_loss, best_t = loss, t
    print(f"  Temperatura óptima ({name}): T={best_t:.2f} (Log-loss: {best_loss:.4f})")
    return round(best_t, 2)


# ====================================================================
# 1. ENTRENAMIENTO
# ====================================================================

def prediccion_oof_temporal(modelo, X, y, pesos, n_splits):
    """Predicciones fuera de muestra con ventana temporal expansiva."""
    pred = np.full(len(X), np.nan, dtype=float)
    for train_idx, valid_idx in TimeSeriesSplit(n_splits=n_splits).split(X):
        estimador = clone(modelo)
        estimador.fit(
            X.iloc[train_idx], y.iloc[train_idx],
            sample_weight=np.asarray(pesos)[train_idx],
        )
        pred[valid_idx] = estimador.predict(X.iloc[valid_idx])
    return pred, ~np.isnan(pred)

def entrenar_modelos():
    df = pd.read_csv('./Data/datos_historicos.csv')
    df['Fecha_dt'] = pd.to_datetime(df['Fecha'])
    df.sort_values('Fecha_dt', inplace=True)
    df.dropna(inplace=True)

    fecha_max = df['Fecha_dt'].max()
    df['Dias_Antiguedad'] = (fecha_max - df['Fecha_dt']).dt.days
    df['Peso_Recencia']   = np.exp(-DECAY_RECENCIA * df['Dias_Antiguedad'])

    df['Resultado_1X2_Num'] = df['Resultado_1X2'].map({'1': 0, 'X': 1, '2': 2})
    y = df['Resultado_1X2_Num']

    cols_a_excluir = [
        'Fecha', 'Fecha_dt', 'Dias_Antiguedad', 'Peso_Recencia',
        'Equipo_Local', 'Equipo_Visitante',
        'Resultado_1X2', 'Resultado_1X2_Num',
        'Goles_Local', 'Goles_Visitante',
        'Valor_Mercado_Millones_Eur_Local', 'Valor_Mercado_Millones_Eur_Visitante',
        'Puntos_Local', 'Puntos_Visitante',   
    ]
    X = df.drop(columns=cols_a_excluir, errors='ignore')

    split_index    = int(len(df) * 0.85)
    X_train        = X.iloc[:split_index];        X_test       = X.iloc[split_index:]
    y_train_1X2    = y.iloc[:split_index];        y_test_1X2   = y.iloc[split_index:]
    y_train_gl     = df['Goles_Local'].iloc[:split_index]
    y_train_gv     = df['Goles_Visitante'].iloc[:split_index]
    peso_rec_train = df['Peso_Recencia'].iloc[:split_index].values
    peso_rec_test  = df['Peso_Recencia'].iloc[split_index:].values

    tscv = TimeSeriesSplit(n_splits=CV_SPLITS)

    print(f"Fase 1: Regresores Tweedie (N_ITER_REG={N_ITER_REG})...")
    pesos_train_L = np.where(y_train_gl >= 3, 1.5, 1.0) * peso_rec_train
    pesos_train_V = np.where(y_train_gv >= 3, 1.5, 1.0) * peso_rec_train

    xgb_reg_L = xgb.XGBRegressor(
        objective='reg:tweedie', tweedie_variance_power=tweedie_parameter, random_state=42,
        tree_method='hist', n_jobs=1,
    )
    xgb_reg_V = xgb.XGBRegressor(
        objective='reg:tweedie', tweedie_variance_power=tweedie_parameter, random_state=42,
        tree_method='hist', n_jobs=1,
    )

    search_L = RandomizedSearchCV(
        xgb_reg_L, PARAM_GRID_REG, cv=tscv, n_iter=N_ITER_REG,
        scoring='neg_mean_poisson_deviance', random_state=42, n_jobs=CPU_THREADS, verbose=1,
    )
    search_V = RandomizedSearchCV(
        xgb_reg_V, PARAM_GRID_REG, cv=tscv, n_iter=N_ITER_REG,
        scoring='neg_mean_poisson_deviance', random_state=42, n_jobs=CPU_THREADS, verbose=1,
    )
    search_L.fit(X_train, y_train_gl, sample_weight=pesos_train_L)
    search_V.fit(X_train, y_train_gv, sample_weight=pesos_train_V)

    mejor_modelo_L = search_L.best_estimator_
    mejor_modelo_V = search_V.best_estimator_
    print("  Params Goles_L:", search_L.best_params_)
    print("  Params Goles_V:", search_V.best_params_)

    print(
        f"\nFase 2: Clasificador 1X2 (N_ITER_1X2={N_ITER_1X2}) + "
        f"calibración {CALIBRATION_METHOD}..."
    )
    # Mantener la escala de inferencia y evitar que el futuro filtre al pasado.
    pred_gl_train, mask_meta = prediccion_oof_temporal(
        mejor_modelo_L, X_train, y_train_gl, pesos_train_L, CV_SPLITS,
    )
    pred_gv_train, mask_meta_v = prediccion_oof_temporal(
        mejor_modelo_V, X_train, y_train_gv, pesos_train_V, CV_SPLITS,
    )
    mask_meta &= mask_meta_v
    pred_gl_test = mejor_modelo_L.predict(X_test)
    pred_gv_test = mejor_modelo_V.predict(X_test)

    X_train_meta = X_train.copy()
    X_train_meta['Pred_Goles_L'] = pred_gl_train
    X_train_meta['Pred_Goles_V'] = pred_gv_train
    X_train_meta = X_train_meta.loc[mask_meta]
    y_train_meta = y_train_1X2.loc[mask_meta]
    peso_train_meta = peso_rec_train[mask_meta]
    X_test_meta = X_test.copy()
    X_test_meta['Pred_Goles_L'] = pred_gl_test
    X_test_meta['Pred_Goles_V'] = pred_gv_test

    xgb_clf_base = xgb.XGBClassifier(
        objective='multi:softprob', num_class=3, base_score=0.5, random_state=42,
        tree_method='hist', n_jobs=1,
    )
    search_1X2 = RandomizedSearchCV(
        xgb_clf_base, PARAM_GRID_1X2, cv=tscv, n_iter=N_ITER_1X2,
        scoring='neg_log_loss', random_state=42, n_jobs=CPU_THREADS, verbose=1,
    )
    search_1X2.fit(X_train_meta, y_train_meta, sample_weight=peso_train_meta)
    print("  Params 1X2:", search_1X2.best_params_)

    calibrado_test = CalibratedClassifierCV(
        estimator=search_1X2.best_estimator_, method=CALIBRATION_METHOD, cv=tscv,
    )
    calibrado_test.fit(X_train_meta, y_train_meta, sample_weight=peso_train_meta)
    pred_test_clases = calibrado_test.predict(X_test_meta)
    probs_test       = calibrado_test.predict_proba(X_test_meta)

    print("\n--- RESULTADOS EN TEST (15% temporal) ---")
    print(classification_report(y_test_1X2, pred_test_clases))
    print(f"Accuracy test: {accuracy_score(y_test_1X2, pred_test_clases):.3f}")

    print("\nOptimizando Temperatura (T)...")
    t_optimo = tunear_temperatura(probs_test, y_test_1X2, name="Histórico Global")

    print("\nFase 3: Reentrenando con el 100% de los datos...")
    y_gl_full     = df['Goles_Local']
    y_gv_full     = df['Goles_Visitante']
    peso_rec_full = df['Peso_Recencia'].values
    pesos_full_L  = np.where(y_gl_full >= 3, 1.5, 1.0) * peso_rec_full
    pesos_full_V  = np.where(y_gv_full >= 3, 1.5, 1.0) * peso_rec_full

    pred_gl_full, mask_full = prediccion_oof_temporal(
        mejor_modelo_L, X, y_gl_full, pesos_full_L, CV_SPLITS,
    )
    pred_gv_full, mask_full_v = prediccion_oof_temporal(
        mejor_modelo_V, X, y_gv_full, pesos_full_V, CV_SPLITS,
    )
    mask_full &= mask_full_v

    X_meta_full = X.copy()
    X_meta_full['Pred_Goles_L'] = pred_gl_full
    X_meta_full['Pred_Goles_V'] = pred_gv_full
    X_meta_1x2 = X_meta_full.loc[mask_full]
    y_meta_1x2 = y.loc[mask_full]
    peso_meta_1x2 = peso_rec_full[mask_full]

    mejor_modelo_L.fit(X, y_gl_full, sample_weight=pesos_full_L)
    mejor_modelo_V.fit(X, y_gv_full, sample_weight=pesos_full_V)

    modelo_1X2_final = xgb.XGBClassifier(
        objective='multi:softprob', num_class=3, base_score=0.5,
        random_state=42, tree_method='hist', n_jobs=1, **search_1X2.best_params_,
    )
    modelo_1X2_final.fit(X_meta_1x2, y_meta_1x2, sample_weight=peso_meta_1x2)
    
    clasificador_calibrado_final = CalibratedClassifierCV(
        estimator=modelo_1X2_final, method=CALIBRATION_METHOD, cv=tscv,
    )
    clasificador_calibrado_final.fit(
        X_meta_1x2, y_meta_1x2, sample_weight=peso_meta_1x2,
    )

    # --- Importancia de las variables Modelo Final --- #
    print("\nTop 25 variables más importantes (Modelo 1X2 Final):")
    # Las columnas del modelo 1X2 son las base + las dos predicciones de la Fase 1
    columnas_1X2 = list(X.columns) + ['Pred_Goles_L', 'Pred_Goles_V']
    
    # Sacamos las importancias del modelo final (no del modelo_L)
    importancias_1X2 = modelo_1X2_final.feature_importances_
    
    df_imp = pd.DataFrame({'Variable': columnas_1X2, 'Importancia': importancias_1X2})
    df_imp = df_imp.sort_values('Importancia', ascending=False).head(25)
    print(df_imp.to_string(index=False))

    df_imp.to_csv('Predicciones/importancia_variables_top25.csv', index=False, encoding='utf-8-sig')

    joblib.dump(mejor_modelo_L,              'modelo_goles_L.pkl')
    joblib.dump(mejor_modelo_V,              'modelo_goles_V.pkl')
    joblib.dump(clasificador_calibrado_final,'modelo_1X2_calibrado.pkl')
    joblib.dump(list(X.columns),             'columnas_entrenamiento.pkl')

    mejores_params = {
        'N_ITER_REG': N_ITER_REG, 'N_ITER_1X2': N_ITER_1X2,
        'N_SIMULACIONES': N_SIMULACIONES,
        'CV_SPLITS': CV_SPLITS, 'CPU_THREADS': CPU_THREADS,
        'CALIBRATION_METHOD': CALIBRATION_METHOD,
        'DECAY_RECENCIA': DECAY_RECENCIA, 'T_OPTIMA_CALCULADA': t_optimo,
        'Goles_L': search_L.best_params_, 'Goles_V': search_V.best_params_,
        '1X2': search_1X2.best_params_,
        'score_GL': float(search_L.best_score_),
        'score_GV': float(search_V.best_score_),
        'score_1X2': float(search_1X2.best_score_),
    }
    with open('Predicciones/mejores_hiperparametros.json', 'w', encoding='utf-8') as f:
        json.dump(mejores_params, f, ensure_ascii=False, indent=2)

    print("\nModelos guardados. ¡Listo para el Mundial!")


# ====================================================================
# 2. PIPELINE DE PREDICCIÓN
# ====================================================================

_CACHE_MODELOS = {}

def _modelos():
    if not _CACHE_MODELOS:
        _CACHE_MODELOS['L']    = joblib.load('modelo_goles_L.pkl')
        _CACHE_MODELOS['V']    = joblib.load('modelo_goles_V.pkl')
        _CACHE_MODELOS['1X2']  = joblib.load('modelo_1X2_calibrado.pkl')
        _CACHE_MODELOS['cols'] = joblib.load('columnas_entrenamiento.pkl')
        if os.path.exists('Predicciones/mejores_hiperparametros.json'):
            with open('Predicciones/mejores_hiperparametros.json', encoding='utf-8') as f:
                _CACHE_MODELOS['t_optima'] = json.load(f).get('T_OPTIMA_CALCULADA', 1.0)
        else:
            _CACHE_MODELOS['t_optima'] = 1.0
    return _CACHE_MODELOS


def _normalizar_modo_cancha(venue_mode, sede_neutral):
    if venue_mode is not None:
        return venue_mode
    return 'neutral' if sede_neutral else 'listed'


def pipeline_prediccion(df_bruto, sede_neutral=True, T=None, venue_mode=None):
    """Predice partidos con tres tratamientos de cancha.

    listed: usa tal cual Equipo_Local/Equipo_Visitante.
    neutral: promedia ida y vuelta para quitar sesgo por orden del fixture.
    host-aware: neutral salvo partidos donde juega EE. UU., Mexico o Canada.
    """
    m = _modelos()
    modelo_L, modelo_V, modelo_1X2, columnas_base = m['L'], m['V'], m['1X2'], m['cols']
    if T is None:
        T = m.get('t_optima', 1.0)
    venue_mode = _normalizar_modo_cancha(venue_mode, sede_neutral)
    if venue_mode not in {'listed', 'neutral', 'host-aware'}:
        raise ValueError("venue_mode debe ser: listed, neutral o host-aware")

    def obtener_predicciones_crudas(df_temp):
        df_calc = df_temp.copy()

        cols_avg_local = [
            c for c in df_calc.columns
            if c.endswith(('_5_Local', '_3_Local', '_2_Local', '_total_Local'))
            and c.startswith('avg_')
        ]
        for col_local in cols_avg_local:
            col_vis = col_local.replace('_Local', '_Visitante')
            if col_vis in df_calc.columns:
                nombre = col_local.replace('_Local', '')
                df_calc[f'diff_{nombre}'] = df_calc[col_local] - df_calc[col_vis]

        for sufijo in ['trend_xG_5', 'avg_xGA_3', 'avg_xGA_5', 'avg_xGA_total',
                        'clean_sheet_rate_5', 'forma_vs_historia']:
            col_l = f'{sufijo}_Local'
            col_v = f'{sufijo}_Visitante'
            if col_l in df_calc.columns and col_v in df_calc.columns:
                df_calc[f'diff_{sufijo}'] = df_calc[col_l] - df_calc[col_v]

        col_pts_l = 'avg_Puntos_total_Local'
        col_pts_v = 'avg_Puntos_total_Visitante'
        if col_pts_l in df_calc.columns and col_pts_v in df_calc.columns:
            df_calc['diff_Puntos']        = df_calc[col_pts_l] - df_calc[col_pts_v]
            df_calc['Prob_Implicita_ELO'] = 1 / (1 + 10 ** (-df_calc['diff_Puntos'] / 400))
            df_calc['diff_Tier']          = (
                df_calc[col_pts_l].apply(asignar_tier)
                - df_calc[col_pts_v].apply(asignar_tier)
            )

        if ('Valor_Mercado_Millones_Eur_Local'    in df_calc.columns and
                'Valor_Mercado_Millones_Eur_Visitante' in df_calc.columns):
            df_calc['diff_Valor_Mercado'] = (
                df_calc['Valor_Mercado_Millones_Eur_Local']
                - df_calc['Valor_Mercado_Millones_Eur_Visitante']
            )

        df_calc['Continente_Local']     = df_calc['Equipo_Local'].map(mapa_continentes)
        df_calc['Continente_Visitante'] = df_calc['Equipo_Visitante'].map(mapa_continentes)
        df_calc['Peso_Local']           = df_calc['Continente_Local'].map(pesos_continente)
        df_calc['Peso_Visitante']       = df_calc['Continente_Visitante'].map(pesos_continente)
        df_calc.drop(['Continente_Local', 'Continente_Visitante'], axis=1, inplace=True)

        for col in columnas_base:
            if col not in df_calc.columns:
                df_calc[col] = 0
        X_listo = df_calc[columnas_base]

        goles_L = modelo_L.predict(X_listo)
        goles_V = modelo_V.predict(X_listo)

        X_meta = X_listo.copy()
        X_meta['Pred_Goles_L'] = goles_L
        X_meta['Pred_Goles_V'] = goles_V
        probs = modelo_1X2.predict_proba(X_meta)
        return goles_L, goles_V, probs

    df_normal    = df_bruto.copy()
    cols_contexto = ['Fecha', 'Equipo_Local', 'Equipo_Visitante']
    if 'Grupo' in df_normal.columns:
        cols_contexto.append('Grupo')
    contexto = df_normal[cols_contexto].copy()

    def aplicar_temperatura(resultados):
        probs_afiladas = resultados[['Prob_Local', 'Prob_Empate', 'Prob_Visitante']] ** (1 / T)
        s = probs_afiladas.sum(axis=1).replace(0, 1e-12)
        resultados[['Prob_Local', 'Prob_Empate', 'Prob_Visitante']] = probs_afiladas.div(s, axis=0)
        return resultados

    goles_L_norm, goles_V_norm, probs_norm = obtener_predicciones_crudas(df_normal)
    df_inverso = df_bruto.copy()
    nuevas_columnas = []
    for col in df_inverso.columns:
        if col.endswith('_Local'):      nuevas_columnas.append(col.replace('_Local',     '_Visitante'))
        elif col.endswith('_Visitante'): nuevas_columnas.append(col.replace('_Visitante', '_Local'))
        else:                           nuevas_columnas.append(col)
    df_inverso.columns = nuevas_columnas
    goles_L_inv, goles_V_inv, probs_inv = obtener_predicciones_crudas(df_inverso)

    resultados = contexto.copy()
    resultados['Modo_Cancha'] = venue_mode

    if venue_mode == 'listed':
        resultados['xG_Modelo_Local']     = goles_L_norm
        resultados['xG_Modelo_Visitante'] = goles_V_norm
        resultados['Prob_Local']          = probs_norm[:, 0]
        resultados['Prob_Empate']         = probs_norm[:, 1]
        resultados['Prob_Visitante']      = probs_norm[:, 2]
    else:
        xg_l_neutral = (goles_L_norm + goles_V_inv) / 2
        xg_v_neutral = (goles_V_norm + goles_L_inv) / 2
        p1_neutral   = (probs_norm[:, 0] + probs_inv[:, 2]) / 2
        px_neutral   = (probs_norm[:, 1] + probs_inv[:, 1]) / 2
        p2_neutral   = (probs_norm[:, 2] + probs_inv[:, 0]) / 2

        resultados['xG_Modelo_Local']     = xg_l_neutral
        resultados['xG_Modelo_Visitante'] = xg_v_neutral
        resultados['Prob_Local']          = p1_neutral
        resultados['Prob_Empate']         = px_neutral
        resultados['Prob_Visitante']      = p2_neutral

        if venue_mode == 'host-aware':
            local_host = resultados['Equipo_Local'].isin(ANFITRIONES_2026)
            visit_host = resultados['Equipo_Visitante'].isin(ANFITRIONES_2026)
            solo_local_host = local_host & ~visit_host
            solo_visit_host = visit_host & ~local_host

            resultados.loc[solo_local_host, 'xG_Modelo_Local'] = goles_L_norm[solo_local_host]
            resultados.loc[solo_local_host, 'xG_Modelo_Visitante'] = goles_V_norm[solo_local_host]
            resultados.loc[solo_local_host, 'Prob_Local'] = probs_norm[solo_local_host, 0]
            resultados.loc[solo_local_host, 'Prob_Empate'] = probs_norm[solo_local_host, 1]
            resultados.loc[solo_local_host, 'Prob_Visitante'] = probs_norm[solo_local_host, 2]

            resultados.loc[solo_visit_host, 'xG_Modelo_Local'] = goles_V_inv[solo_visit_host]
            resultados.loc[solo_visit_host, 'xG_Modelo_Visitante'] = goles_L_inv[solo_visit_host]
            resultados.loc[solo_visit_host, 'Prob_Local'] = probs_inv[solo_visit_host, 2]
            resultados.loc[solo_visit_host, 'Prob_Empate'] = probs_inv[solo_visit_host, 1]
            resultados.loc[solo_visit_host, 'Prob_Visitante'] = probs_inv[solo_visit_host, 0]

    resultados['xG_Modelo_Local'] = (resultados['xG_Modelo_Local'] * FACTOR_GOL_DINAMICO).round(2)
    resultados['xG_Modelo_Visitante'] = (resultados['xG_Modelo_Visitante'] * FACTOR_GOL_DINAMICO).round(2)
    return aplicar_temperatura(resultados)


# ====================================================================
# 3. CARGA DEL MUNDIAL
# ====================================================================

def cargar_mundial():
    df_mundial = pd.read_csv('./Data/partidos_mundial.csv')[
        ['Fecha', 'Equipo_Local', 'Equipo_Visitante']
    ]
    df_vars = pd.read_csv('./Data/datos_mundial.csv').sort_values('Fecha')
    grupos  = pd.read_csv('./Data/Grupos_Mundial.csv', sep=';')

    aux = df_mundial.merge(df_vars, left_on='Equipo_Local',    right_on='Equipo', how='left')
    df_mundial_vars = aux.merge(
        df_vars, left_on='Equipo_Visitante', right_on='Equipo', how='left',
    )
    df_mundial_vars.drop(
        columns=[c for c in df_mundial_vars.columns
                 if c in ('Equipo_x', 'Equipo_y', 'Fecha_x', 'Fecha_y',
                           'Resultado_1X2_x', 'Resultado_1X2_y',
                           'Tipo_Equipo_x', 'Tipo_Equipo_y')],
        inplace=True, errors='ignore',
    )
    df_mundial_vars.columns = df_mundial_vars.columns.str.replace(r'_x$', '_Local',    regex=True)
    df_mundial_vars.columns = df_mundial_vars.columns.str.replace(r'_y$', '_Visitante', regex=True)

    df_mundial_grupos = pd.merge(
        df_mundial_vars, grupos, left_on='Equipo_Local', right_on='Equipo',
    ).drop('Equipo', axis=1)

    fechas_reales = pd.read_csv('./Data/partidos_mundial.csv')[
        ['Fecha', 'Equipo_Local', 'Equipo_Visitante']
    ]
    return df_mundial_grupos, df_vars, grupos, fechas_reales


def aplicar_resultados_reales(df_pred, ruta=None):
    """Fija partidos ya jugados para la tabla y el Monte Carlo."""
    global FACTOR_GOL_DINAMICO
    ruta = ruta or RUTA_RESULTADOS_REALES
    df = df_pred.copy()
    df['Jugado'] = False

    if not ruta or not os.path.exists(ruta):
        return df

    reales = pd.read_csv(ruta)
    if reales.empty:
        return df

    alias_equipos = {
        'Arabia Saudita': 'Arabia Saudí',
        'Bosnia y Herzegovina': 'Bosnia-Herzegovina',
        'Estados Unidos': 'EE. UU.',
        'Qatar': 'Catar',
    }
    for col in ['Equipo_Local', 'Equipo_Visitante']:
        if col in reales.columns:
            reales[col] = reales[col].replace(alias_equipos)

    requeridas = {
        'Equipo_Local', 'Equipo_Visitante', 'Goles_Local', 'Goles_Visitante',
    }
    faltantes = requeridas - set(reales.columns)
    if faltantes:
        raise ValueError(f"Faltan columnas en {ruta}: {', '.join(sorted(faltantes))}")

    claves = ['Equipo_Local', 'Equipo_Visitante']
    if reales.duplicated(claves).any():
        raise ValueError(f'Hay partidos duplicados en {ruta}.')

    calendario = set(map(tuple, df[claves].to_numpy()))
    desconocidos = [tuple(x) for x in reales[claves].to_numpy()
                    if tuple(x) not in calendario]
    if desconocidos:
        raise ValueError(f'Partidos no encontrados en el calendario: {desconocidos}')

    for col in ['Goles_Local', 'Goles_Visitante']:
        reales[col] = pd.to_numeric(reales[col], errors='raise')
        if (reales[col] < 0).any() or (reales[col] % 1 != 0).any():
            raise ValueError(f'{col} debe contener enteros no negativos.')

    reales = reales[claves + ['Goles_Local', 'Goles_Visitante']].rename(columns={
        'Goles_Local': 'Goles_Reales_Local',
        'Goles_Visitante': 'Goles_Reales_Visitante',
    })
    df = df.merge(reales, on=claves, how='left', validate='one_to_one')
    jugado = df['Goles_Reales_Local'].notna()
    df['Jugado'] = jugado

    df['xG_Modelo_Local_Previa'] = df['xG_Modelo_Local']
    df['xG_Modelo_Visitante_Previa'] = df['xG_Modelo_Visitante']
    for col in ['Prob_Local', 'Prob_Empate', 'Prob_Visitante']:
        df[f'{col}_Previa'] = df[col]

    gl = df['Goles_Reales_Local']
    gv = df['Goles_Reales_Visitante']
    xg_previo_total = (
        df.loc[jugado, 'xG_Modelo_Local_Previa']
        + df.loc[jugado, 'xG_Modelo_Visitante_Previa']
    ).sum()
    goles_reales_total = (gl[jugado] + gv[jugado]).sum()
    if xg_previo_total > 0 and goles_reales_total > 0:
        FACTOR_GOL_DINAMICO = float(np.clip(
            goles_reales_total / xg_previo_total,
            FACTOR_GOL_MIN,
            FACTOR_GOL_MAX,
        ))
        pendientes = ~jugado
        df.loc[pendientes, 'xG_Modelo_Local'] *= FACTOR_GOL_DINAMICO
        df.loc[pendientes, 'xG_Modelo_Visitante'] *= FACTOR_GOL_DINAMICO

    df.loc[jugado, 'Prob_Local'] = (gl[jugado] > gv[jugado]).astype(float)
    df.loc[jugado, 'Prob_Empate'] = (gl[jugado] == gv[jugado]).astype(float)
    df.loc[jugado, 'Prob_Visitante'] = (gl[jugado] < gv[jugado]).astype(float)
    df.loc[jugado, 'xG_Modelo_Local'] = gl[jugado]
    df.loc[jugado, 'xG_Modelo_Visitante'] = gv[jugado]

    print(
        f'Resultados reales aplicados: {int(jugado.sum())} partido(s). '
        f'Factor goles={FACTOR_GOL_DINAMICO:.2f}.'
    )
    return df


def comparar_modos_cancha(df_mundial_grupos, T_grupos):
    base = pipeline_prediccion(df_mundial_grupos, T=T_grupos, venue_mode='neutral')
    listado = pipeline_prediccion(df_mundial_grupos, T=T_grupos, venue_mode='listed')
    anfitrion = pipeline_prediccion(df_mundial_grupos, T=T_grupos, venue_mode='host-aware')

    cols = ['Fecha', 'Equipo_Local', 'Equipo_Visitante']
    comp = base[cols].copy()
    comp['Prob_Local_Neutral'] = (base['Prob_Local'] * 100).round(1)
    comp['Prob_Empate_Neutral'] = (base['Prob_Empate'] * 100).round(1)
    comp['Prob_Visitante_Neutral'] = (base['Prob_Visitante'] * 100).round(1)
    comp['Prob_Local_HostAware'] = (anfitrion['Prob_Local'] * 100).round(1)
    comp['Prob_Empate_HostAware'] = (anfitrion['Prob_Empate'] * 100).round(1)
    comp['Prob_Visitante_HostAware'] = (anfitrion['Prob_Visitante'] * 100).round(1)
    comp['Prob_Local_Listed'] = (listado['Prob_Local'] * 100).round(1)
    comp['Prob_Empate_Listed'] = (listado['Prob_Empate'] * 100).round(1)
    comp['Prob_Visitante_Listed'] = (listado['Prob_Visitante'] * 100).round(1)
    comp['Delta_Local_pp'] = (
        comp['Prob_Local_HostAware'] - comp['Prob_Local_Neutral']
    ).round(1)
    comp['Delta_Visitante_pp'] = (
        comp['Prob_Visitante_HostAware'] - comp['Prob_Visitante_Neutral']
    ).round(1)
    comp['Sesgo_Local_Listed_vs_Neutral_pp'] = (
        comp['Prob_Local_Listed'] - comp['Prob_Local_Neutral']
    ).round(1)
    comp['Anfitrion_Involucrado'] = (
        comp['Equipo_Local'].isin(ANFITRIONES_2026)
        | comp['Equipo_Visitante'].isin(ANFITRIONES_2026)
    )
    comp.to_csv('Predicciones/comparacion_modos_cancha.csv', index=False, encoding='utf-8-sig')
    return comp


# ====================================================================
# 4. MATRIZ DE CRUCES 48x48
# ====================================================================

def matriz_cruces(equipos, df_vars, T_cruces, venue_mode='neutral'):
    # CORRECCIÓN VITAL: Quitamos 'Fecha' de df_vars antes del merge para evitar colisiones 
    # de columnas (Fecha_x y Fecha_y) que romperían el pipeline_prediccion.
    df_vars_clean = df_vars.drop(columns=['Fecha'], errors='ignore')

    pares       = [(a, b) for a in equipos for b in equipos if a != b]
    partido     = pd.DataFrame({
        'Fecha':            ['2026-07-01'] * len(pares),
        'Equipo_Local':    [a for a, b in pares],
        'Equipo_Visitante': [b for a, b in pares],
    })
    partido_vars = partido.merge(df_vars_clean, left_on='Equipo_Local',    right_on='Equipo', how='left').drop(columns=['Equipo'])
    partido_vars = partido_vars.merge(df_vars_clean, left_on='Equipo_Visitante', right_on='Equipo', how='left',
                                      suffixes=('_Local', '_Visitante')).drop(columns=['Equipo'])
    
    df_pred = pipeline_prediccion(partido_vars, T=T_cruces, venue_mode=venue_mode)

    idx = {e: i for i, e in enumerate(equipos)}
    n   = len(equipos)
    P1  = np.zeros((n, n)); PX = np.zeros((n, n)); P2  = np.zeros((n, n))
    XGL = np.zeros((n, n)); XGV = np.zeros((n, n))

    for (a, b), (_, r) in zip(pares, df_pred.iterrows()):
        i, j   = idx[a], idx[b]
        s      = r['Prob_Local'] + r['Prob_Empate'] + r['Prob_Visitante']
        P1[i, j]  = r['Prob_Local']    / s
        PX[i, j]  = r['Prob_Empate']   / s
        P2[i, j]  = r['Prob_Visitante'] / s
        XGL[i, j] = r['xG_Modelo_Local']
        XGV[i, j] = r['xG_Modelo_Visitante']

    M_adv = P1 + PX * (P1 / np.where(P1 + P2 == 0, 1, P1 + P2))
    np.fill_diagonal(M_adv, 0.5)
    return {'P1': P1, 'PX': PX, 'P2': P2, 'XGL': XGL, 'XGV': XGV, 'M_adv': M_adv, 'idx': idx}


# ====================================================================
# 5. UTILIDADES DE PREDICCIÓN PUNTUAL
# ====================================================================

def _poisson_pmf(k, lam):
    lam = max(lam, 0.05)
    return math.exp(-lam) * lam ** k / math.factorial(k)


def marcador_mas_probable(xg_l, xg_v, prob_1, prob_x, prob_2, resultado, agresividad=.5):
    """
    Calcula el marcador usando Poisson, inflando los xG dinámicamente
    en base a la probabilidad real (0.0 a 1.0) de victoria de cada equipo.
    """
    # ESCALADO DINÁMICO: Multiplicamos el xG base por (1 + probabilidad * agresividad)
    # Ejemplo: Si prob_1 es 0.90 (90%), su xG se multiplica por (1 + 0.90*1.2) = 2.08 (¡Sube más del doble!)
    # Si prob_2 es 0.20 (20%), su xG se multiplica por (1 + 0.20*1.2) = 1.24 (Sube un poco por agresividad)
    lam_l = xg_l
    lam_v = xg_v
    if prob_1 > prob_2:
        lam_l = max(xg_l * (1 + (prob_1 * agresividad)), 0.1)
    if prob_2 > prob_1:
        lam_v = max(xg_v * (1 + (prob_2 * agresividad)), 0.1)
    
    # TRATAMIENTO DEL EMPATE: Si el resultado predicho es 'X', empujamos ambos xG 
    # en función de lo fuerte que sea esa probabilidad de empate (para evitar el 0-0 eterno)
    if resultado == 'X':
        empuje_empate = prob_x * 0.6
        lam_l += empuje_empate
        lam_v += empuje_empate

    mejor, p_mejor = (0, 0), -1.0
    for i in range(9):
        for j in range(9):
            if resultado == '1' and not i > j: continue
            if resultado == 'X' and i != j:   continue
            if resultado == '2' and not i < j: continue
            
            p = _poisson_pmf(i, lam_l) * _poisson_pmf(j, lam_v)
                
            if p > p_mejor:
                mejor, p_mejor = (i, j), p
                
    return mejor


# ====================================================================
# 6. CLASIFICACIÓN DE GRUPOS
# ====================================================================

CRUCES_R32 = [
    ('1E', '3_1'), ('1I', '3_2'), ('2A', '2B'), ('1F', '2C'),
    ('2K', '2L'), ('1H', '2J'), ('1D', '3_3'), ('1G', '3_4'),
    ('1C', '2F'), ('2E', '2I'), ('1A', '3_5'), ('1L', '3_6'),
    ('1J', '2H'), ('2D', '2G'), ('1B', '3_7'), ('1K', '3_8'),
]


def clasificar_grupos(df, tiradas):
    df  = df.copy()
    tir = np.asarray(tiradas)
    df['Pts_L'] = np.where(tir == 0, 3, np.where(tir == 1, 1, 0))
    df['Pts_V'] = np.where(tir == 2, 3, np.where(tir == 1, 1, 0))

    locales    = df[['Grupo', 'Equipo_Local',    'Pts_L', 'xG_Modelo_Local',    'xG_Modelo_Visitante']].rename(
        columns={'Equipo_Local':    'Equipo', 'Pts_L': 'Pts', 'xG_Modelo_Local':    'GF', 'xG_Modelo_Visitante': 'GC'})
    visitantes = df[['Grupo', 'Equipo_Visitante', 'Pts_V', 'xG_Modelo_Visitante', 'xG_Modelo_Local']].rename(
        columns={'Equipo_Visitante': 'Equipo', 'Pts_V': 'Pts', 'xG_Modelo_Visitante': 'GF', 'xG_Modelo_Local': 'GC'})

    clasif = pd.concat([locales, visitantes])
    clasif['DG'] = clasif['GF'] - clasif['GC']
    clasif = clasif.groupby(['Grupo', 'Equipo']).sum().reset_index()
    clasif = clasif.sort_values(['Grupo', 'Pts', 'DG', 'GF'], ascending=[True, False, False, False])
    clasif['Posicion'] = clasif.groupby('Grupo').cumcount() + 1

    terceros = clasif[clasif['Posicion'] == 3].sort_values(['Pts', 'DG', 'GF'], ascending=False).head(8)
    pos = {f"{r['Posicion']}{r['Grupo']}": r['Equipo'] for _, r in clasif[clasif['Posicion'] <= 2].iterrows()}
    for i, eq in enumerate(terceros['Equipo']): pos[f'3_{i + 1}'] = eq
    return clasif, terceros, pos


# ====================================================================
# 7. MONTE CARLO VECTORIZADO
# ====================================================================

def monte_carlo(df_pred_grupos, mc, equipos, n_sims=N_SIMULACIONES):
    idx  = mc['idx']
    n_eq = len(equipos)
    df   = df_pred_grupos

    eq_grupo = pd.concat([
        df[['Grupo', 'Equipo_Local']].rename(columns={'Equipo_Local': 'Equipo'}),
        df[['Grupo', 'Equipo_Visitante']].rename(columns={'Equipo_Visitante': 'Equipo'}),
    ]).drop_duplicates()
    grupos_de = {r['Equipo']: r['Grupo'] for _, r in eq_grupo.iterrows()}
    letras    = sorted(eq_grupo['Grupo'].unique())
    miembros  = {g: sorted([e for e, gg in grupos_de.items() if gg == g]) for g in letras}

    loc_series = df['Equipo_Local'].map(idx)
    vis_series = df['Equipo_Visitante'].map(idx)

    if loc_series.isna().any() or vis_series.isna().any():
        raise ValueError(
            f"Equipos sin índice — revisa Grupos_Mundial.csv.\n"
            f"  Locales: {df[loc_series.isna()]['Equipo_Local'].unique()}\n"
            f"  Visitantes: {df[vis_series.isna()]['Equipo_Visitante'].unique()}"
        )

    loc = loc_series.astype(int).to_numpy()
    vis = vis_series.astype(int).to_numpy()

    P    = df[['Prob_Local', 'Prob_Empate', 'Prob_Visitante']].to_numpy()
    P    = P / P.sum(axis=1, keepdims=True)
    xg_l = df['xG_Modelo_Local'].to_numpy()
    xg_v = df['xG_Modelo_Visitante'].to_numpy()

    gf = np.zeros(n_eq); gc = np.zeros(n_eq)
    np.add.at(gf, loc, xg_l); np.add.at(gf, vis, xg_v)
    np.add.at(gc, loc, xg_v); np.add.at(gc, vis, xg_l)
    dg   = gf - gc
    dg_c = np.round(dg * 100).astype(np.int64)
    gf_c = np.round(gf * 100).astype(np.int64)

    u    = np.random.random((n_sims, len(df)))
    cum1 = P[:, 0]; cum2 = P[:, 0] + P[:, 1]
    out  = np.where(u < cum1, 0, np.where(u < cum2, 1, 2)).astype(np.int8)

    pts = np.zeros((n_sims, n_eq), dtype=np.int64)
    for m_idx in range(len(df)):
        o = out[:, m_idx]
        pts[:, loc[m_idx]] += np.where(o == 0, 3, np.where(o == 1, 1, 0))
        pts[:, vis[m_idx]] += np.where(o == 2, 3, np.where(o == 1, 1, 0))

    clave = pts * 10_000_000_000 + (dg_c[None, :] + 100_000) * 10_000 + gf_c[None, :]

    pos_eq         = {}
    terceros_ids   = np.zeros((n_sims, 12), dtype=np.int64)
    terceros_clave = np.zeros((n_sims, 12), dtype=np.int64)
    for gi, g in enumerate(letras):
        ids      = np.array([idx[e] for e in miembros[g]])
        k        = clave[:, ids]
        orden    = np.argsort(-k, axis=1, kind='stable')
        ordenados = ids[orden]
        pos_eq[f'1{g}']       = ordenados[:, 0]
        pos_eq[f'2{g}']       = ordenados[:, 1]
        terceros_ids[:, gi]   = ordenados[:, 2]
        terceros_clave[:, gi] = np.take_along_axis(k, orden[:, 2:3], axis=1)[:, 0]

    orden_terceros = np.argsort(-terceros_clave, axis=1, kind='stable')
    mejores8       = np.take_along_axis(terceros_ids, orden_terceros[:, :8], axis=1)
    for r in range(8): pos_eq[f'3_{r + 1}'] = mejores8[:, r]

    M          = mc['M_adv']
    contadores = {f: np.zeros(n_eq, dtype=np.int64)
                  for f in ['R32', 'Octavos', 'Cuartos', 'Semis', 'Final', 'Campeon']}

    clasificados = np.stack(
        [pos_eq[f'1{g}'] for g in letras] +
        [pos_eq[f'2{g}'] for g in letras] +
        [mejores8[:, r]  for r in range(8)],
        axis=1,
    )
    for c in range(32): np.add.at(contadores['R32'], clasificados[:, c], 1)

    def jugar(a_ids, b_ids):
        p      = M[a_ids, b_ids]
        gana_a = np.random.random(a_ids.shape) < p
        return np.where(gana_a, a_ids, b_ids)

    r32 = [(pos_eq[a], pos_eq[b]) for a, b in CRUCES_R32]
    g32 = [jugar(a, b) for a, b in r32]
    for w in g32: np.add.at(contadores['Octavos'], w, 1)
    g16 = [jugar(g32[i], g32[i + 1]) for i in range(0, 16, 2)]
    for w in g16: np.add.at(contadores['Cuartos'], w, 1)
    gqf = [jugar(g16[i], g16[i + 1]) for i in range(0, 8, 2)]
    for w in gqf: np.add.at(contadores['Semis'], w, 1)
    sf1 = jugar(gqf[0], gqf[1]); sf2 = jugar(gqf[2], gqf[3])
    for w in (sf1, sf2): np.add.at(contadores['Final'], w, 1)
    campeon = jugar(sf1, sf2)
    np.add.at(contadores['Campeon'], campeon, 1)

    tabla = pd.DataFrame(
        {f: contadores[f] / n_sims * 100 for f in contadores}, index=equipos,
    )
    return tabla.sort_values(['Campeon', 'Final', 'Semis'], ascending=False).round(1)


# ====================================================================
# 8. PREDICCIÓN PUNTUAL DE TODO EL MUNDIAL
# ====================================================================

FASES_FECHAS = {
    'Dieciseisavos': '28 jun - 3 jul', 'Octavos': '4 - 7 jul', 'Cuartos': '9 - 11 jul',
    'Semifinales':   '14 - 15 jul',    '3er Puesto': '18 jul', 'Final': '19 jul',
}


def prediccion_puntual(df_pred_grupos, mc, equipos, fechas_reales):
    idx     = mc['idx']
    probs   = df_pred_grupos[['Prob_Local', 'Prob_Empate', 'Prob_Visitante']].to_numpy()
    tiradas = probs.argmax(axis=1)

    filas       = []
    mapa_fechas = {(r['Equipo_Local'], r['Equipo_Visitante']): r['Fecha']
                   for _, r in fechas_reales.iterrows()}

    # BUCLE 1: FASE DE GRUPOS
    for k, (_, r) in enumerate(df_pred_grupos.iterrows()):
        res    = ['1', 'X', '2'][tiradas[k]]
        probs_previas = [
            r.get('Prob_Local_Previa', r['Prob_Local']),
            r.get('Prob_Empate_Previa', r['Prob_Empate']),
            r.get('Prob_Visitante_Previa', r['Prob_Visitante']),
        ]
        res_previo = ['1', 'X', '2'][int(np.argmax(probs_previas))]
        xg_l_previo = r.get('xG_Modelo_Local_Previa', r['xG_Modelo_Local'])
        xg_v_previo = r.get('xG_Modelo_Visitante_Previa', r['xG_Modelo_Visitante'])
        gl_previo, gv_previo = marcador_mas_probable(
            xg_l_previo, xg_v_previo,
            probs_previas[0], probs_previas[1], probs_previas[2],
            res_previo,
        )

        if bool(r.get('Jugado', False)):
            gl = int(r['Goles_Reales_Local'])
            gv = int(r['Goles_Reales_Visitante'])
            estado = 'Jugado'
        else:
            gl, gv = marcador_mas_probable(
                r['xG_Modelo_Local'], r['xG_Modelo_Visitante'],
                r['Prob_Local'], r['Prob_Empate'], r['Prob_Visitante'],
                res
            )
            estado = 'Pendiente'
        
        filas.append({
            'Fecha':             mapa_fechas.get((r['Equipo_Local'], r['Equipo_Visitante']), ''),
            'Grupo':             r['Grupo'],
            'Local':             r['Equipo_Local'],
            'Visitante':         r['Equipo_Visitante'],
            'Marcador_Predicho': f'{gl}-{gv}',
            'Estado':            estado,
            'Resultado_1X2':     res,
            'Marcador_Modelo_Previo': f'{gl_previo}-{gv_previo}',
            'Resultado_1X2_Modelo_Previo': res_previo,
            'xG_L':              round(r['xG_Modelo_Local'],    2),
            'xG_V':              round(r['xG_Modelo_Visitante'], 2),
            'xG_L_Modelo_Previo': round(xg_l_previo, 2),
            'xG_V_Modelo_Previo': round(xg_v_previo, 2),
            'Prob_1':            round(r['Prob_Local']    * 100, 1),
            'Prob_X':            round(r['Prob_Empate']   * 100, 1),
            'Prob_2':            round(r['Prob_Visitante'] * 100, 1),
            'Prob_1_Modelo_Previo': round(probs_previas[0] * 100, 1),
            'Prob_X_Modelo_Previo': round(probs_previas[1] * 100, 1),
            'Prob_2_Modelo_Previo': round(probs_previas[2] * 100, 1),
        })

    df_grupos_pred = pd.DataFrame(filas).sort_values(['Grupo', 'Fecha']).reset_index(drop=True)
    clasif, terceros, pos = clasificar_grupos(df_pred_grupos, tiradas)

    P1, PX, P2, XGL, XGV = mc['P1'], mc['PX'], mc['P2'], mc['XGL'], mc['XGV']
    registro = []

    # BUCLE 2: ELIMINATORIAS (CRUCES)
    def jugar_cruce(fase, eq_a, eq_b):
        i, j       = idx[eq_a], idx[eq_b]
        p1, px, p2 = P1[i, j], PX[i, j], P2[i, j]
        res        = ['1', 'X', '2'][int(np.argmax([p1, px, p2]))]
        
        if res == 'X':
            ganador  = eq_a if p1 >= p2 else eq_b
            # Pasamos p1, px, p2 a la función en caso de empate
            gl, gv   = marcador_mas_probable(XGL[i, j], XGV[i, j], p1, px, p2, 'X')
            marcador = f'{gl}-{gv} (pen)'
            detalle  = 'Empate; gana en penaltis'
        else:
            ganador  = eq_a if res == '1' else eq_b
            # Pasamos p1, px, p2 a la función en caso de victoria clara
            gl, gv   = marcador_mas_probable(XGL[i, j], XGV[i, j], p1, px, p2, res)
            marcador = f'{gl}-{gv}'
            detalle  = 'Tiempo regular'
            
        registro.append({
            'Fase': fase, 'Fechas': FASES_FECHAS[fase],
            'Local': eq_a, 'Visitante': eq_b,
            'Marcador_Predicho': marcador, 'Avanza': ganador,
            'xG_L': round(XGL[i, j], 2), 'xG_V': round(XGV[i, j], 2),
            'Prob_1': round(p1 * 100, 1), 'Prob_X': round(px * 100, 1),
            'Prob_2': round(p2 * 100, 1), 'Detalle': detalle,
        })
        return ganador

    g32 = [jugar_cruce('Dieciseisavos', pos[a], pos[b]) for a, b in CRUCES_R32]
    g16 = [jugar_cruce('Octavos',       g32[i], g32[i + 1]) for i in range(0, 16, 2)]
    gqf = [jugar_cruce('Cuartos',       g16[i], g16[i + 1]) for i in range(0, 8,  2)]
    sf  = [jugar_cruce('Semifinales', gqf[0], gqf[1]),
           jugar_cruce('Semifinales', gqf[2], gqf[3])]
    perdedores_sf = [e for par in [(gqf[0], gqf[1]), (gqf[2], gqf[3])] for e in par if e not in sf]
    jugar_cruce('3er Puesto', perdedores_sf[0], perdedores_sf[1])
    campeon = jugar_cruce('Final', sf[0], sf[1])

    return df_grupos_pred, clasif, terceros, pos, pd.DataFrame(registro), campeon


def _resultado_1x2_desde_goles(gl, gv):
    if gl > gv:
        return '1'
    if gl == gv:
        return 'X'
    return '2'


def _parse_marcador(marcador):
    gl, gv = str(marcador).split('-')
    return int(gl), int(gv)


def generar_validacion_predicciones(df_grupos_pred):
    jugados = df_grupos_pred[df_grupos_pred['Estado'] == 'Jugado'].copy()
    if jugados.empty:
        return pd.DataFrame()

    filas = []
    for _, r in jugados.iterrows():
        gl_real, gv_real = _parse_marcador(r['Marcador_Predicho'])
        gl_pred, gv_pred = _parse_marcador(r['Marcador_Modelo_Previo'])
        res_real = _resultado_1x2_desde_goles(gl_real, gv_real)
        res_pred = r['Resultado_1X2_Modelo_Previo']

        probs = {
            '1': float(r['Prob_1_Modelo_Previo']) / 100,
            'X': float(r['Prob_X_Modelo_Previo']) / 100,
            '2': float(r['Prob_2_Modelo_Previo']) / 100,
        }
        brier = sum((probs[k] - (1.0 if k == res_real else 0.0)) ** 2 for k in ['1', 'X', '2'])
        prob_real = probs[res_real] * 100

        filas.append({
            'Fecha': r['Fecha'],
            'Grupo': r['Grupo'],
            'Local': r['Local'],
            'Visitante': r['Visitante'],
            'Marcador_Modelo_Previo': r['Marcador_Modelo_Previo'],
            'Marcador_Real': r['Marcador_Predicho'],
            'Resultado_Modelo_Previo': res_pred,
            'Resultado_Real': res_real,
            'Acierto_1X2': res_pred == res_real,
            'Acierto_Marcador': (gl_pred, gv_pred) == (gl_real, gv_real),
            'Prob_Real_Modelo_Previo': round(prob_real, 1),
            'Sorpresa_pp': round(100 - prob_real, 1),
            'Error_Goles_Local': abs(gl_pred - gl_real),
            'Error_Goles_Visitante': abs(gv_pred - gv_real),
            'Error_Goles_Total': abs(gl_pred - gl_real) + abs(gv_pred - gv_real),
            'Brier_1X2': round(brier, 4),
            'Prob_1_Modelo_Previo': r['Prob_1_Modelo_Previo'],
            'Prob_X_Modelo_Previo': r['Prob_X_Modelo_Previo'],
            'Prob_2_Modelo_Previo': r['Prob_2_Modelo_Previo'],
        })

    val = pd.DataFrame(filas).sort_values(['Fecha', 'Grupo']).reset_index(drop=True)
    val.to_csv('Predicciones/validacion_predicciones.csv', index=False, encoding='utf-8-sig')

    n = len(val)
    acc_1x2 = val['Acierto_1X2'].mean() * 100
    acc_marcador = val['Acierto_Marcador'].mean() * 100
    mae_total = val['Error_Goles_Total'].mean()
    brier = val['Brier_1X2'].mean()
    prob_real_media = val['Prob_Real_Modelo_Previo'].mean()

    lineas = [
        '# Validacion de predicciones vs resultados reales',
        '',
        'Compara la prediccion previa del modelo contra los partidos ya jugados. '
        'Los partidos jugados se fijan despues para tablas y Monte Carlo, pero aqui se evalua '
        'lo que el modelo habia dicho antes de conocer el marcador real.',
        '',
        '## Resumen',
        '',
        '| Metrica | Valor |',
        '|---|---:|',
        f'| Partidos evaluados | {n} |',
        f'| Acierto 1X2 | {acc_1x2:.1f}% |',
        f'| Marcador exacto | {acc_marcador:.1f}% |',
        f'| Error medio de goles totales | {mae_total:.2f} |',
        f'| Brier score 1X2 medio | {brier:.3f} |',
        f'| Probabilidad media asignada al resultado real | {prob_real_media:.1f}% |',
        '',
        '## Mayores sorpresas',
        '',
        '| Fecha | Partido | Prediccion previa | Real | Prob. real previa |',
        '|---|---|---:|---:|---:|',
    ]
    sorpresas = val.sort_values('Prob_Real_Modelo_Previo').head(10)
    for _, r in sorpresas.iterrows():
        lineas.append(
            f"| {r['Fecha']} | {r['Local']} - {r['Visitante']} | "
            f"{r['Marcador_Modelo_Previo']} ({r['Resultado_Modelo_Previo']}) | "
            f"{r['Marcador_Real']} ({r['Resultado_Real']}) | "
            f"{r['Prob_Real_Modelo_Previo']:.1f}% |"
        )
    lineas.extend([
        '',
        '## Detalle',
        '',
        '| Fecha | Grupo | Partido | Pred. previa | Real | Acierto 1X2 | Prob. real previa | Brier |',
        '|---|---|---|---:|---:|:-:|---:|---:|',
    ])
    for _, r in val.iterrows():
        ok = 'si' if r['Acierto_1X2'] else 'no'
        lineas.append(
            f"| {r['Fecha']} | {r['Grupo']} | {r['Local']} - {r['Visitante']} | "
            f"{r['Marcador_Modelo_Previo']} | {r['Marcador_Real']} | {ok} | "
            f"{r['Prob_Real_Modelo_Previo']:.1f}% | {r['Brier_1X2']:.3f} |"
        )
    with open('Predicciones/VALIDACION.md', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lineas) + '\n')

    print(
        f"Validacion: {n} jugados | acierto 1X2={acc_1x2:.1f}% | "
        f"marcador exacto={acc_marcador:.1f}% | Brier={brier:.3f}"
    )
    return val


# ====================================================================
# MAIN
# ====================================================================

def parsear_argumentos():
    parser = argparse.ArgumentParser(description='Prediccion Mundial 2026')
    parser.add_argument('--profile', choices=['full', 'colab', 'test'], default='colab')
    parser.add_argument('--n-sims', type=int, help='Sobrescribe el numero de simulaciones.')
    parser.add_argument('--force-retrain', action='store_true')
    parser.add_argument('--results', default=RUTA_RESULTADOS_REALES,
                        help='CSV opcional con resultados reales de fase de grupos.')
    parser.add_argument(
        '--venue-mode', choices=['neutral', 'host-aware', 'listed'], default='host-aware',
        help='Tratamiento de cancha: neutral, host-aware o listed.',
    )
    return parser.parse_args()

if __name__ == '__main__':
    args = parsear_argumentos()
    configurar_perfil(args.profile)
    if args.n_sims is not None:
        if args.n_sims < 1:
            raise ValueError('--n-sims debe ser mayor que cero.')
        N_SIMULACIONES = args.n_sims
    if args.force_retrain:
        FORZAR_REENTRENAMIENTO = True

    print(
        f"Perfil={args.profile} | CPU={CPU_THREADS} | CV={CV_SPLITS} | "
        f"iter reg={N_ITER_REG} | iter 1X2={N_ITER_1X2} | sims={N_SIMULACIONES} | "
        f"cancha={args.venue_mode}"
    )

    pkls         = ['modelo_goles_L.pkl', 'modelo_goles_V.pkl',
                    'modelo_1X2_calibrado.pkl', 'columnas_entrenamiento.pkl']
    pkls_existen = all(os.path.exists(p) for p in pkls)

    if FORZAR_REENTRENAMIENTO and pkls_existen:
        print("FORZAR_REENTRENAMIENTO=True — reentrenando...")
        entrenar_modelos()
    elif not pkls_existen:
        print("No se encontraron .pkl — entrenando desde cero...")
        entrenar_modelos()
    else:
        print("Modelos .pkl encontrados — reutilizando.")

    m        = _modelos()
    T_OPTIMA = m.get('t_optima', 1.0)
    T_GRUPOS = T_OPTIMA * T_FORZADA
    T_CRUCES = T_OPTIMA * T_FORZADA

    print(f"\nFase de grupos (T={T_GRUPOS})...")
    df_mundial_grupos, df_vars, grupos, fechas_reales = cargar_mundial()
    comparar_modos_cancha(df_mundial_grupos, T_GRUPOS)
    df_predicciones_mundial = pipeline_prediccion(
        df_mundial_grupos, T=T_GRUPOS, venue_mode=args.venue_mode,
    )
    df_predicciones_mundial['Grupo'] = df_mundial_grupos['Grupo'].values
    df_predicciones_mundial = aplicar_resultados_reales(
        df_predicciones_mundial, args.results,
    )

    equipos = sorted(grupos['Equipo'].unique())
    print(f"Matriz de cruces 48×48 (T={T_CRUCES})...")
    mc = matriz_cruces(equipos, df_vars, T_CRUCES, venue_mode=args.venue_mode)

    print("Predicción puntual de los 104 partidos...")
    df_grupos_pred, clasif, terceros, pos, df_elim, campeon = prediccion_puntual(
        df_predicciones_mundial, mc, equipos, fechas_reales,
    )
    generar_validacion_predicciones(df_grupos_pred)

    print(f"Monte Carlo ({N_SIMULACIONES} simulaciones)...")
    tabla_mc = monte_carlo(df_predicciones_mundial, mc, equipos, N_SIMULACIONES)

    df_grupos_pred.sort_values('Fecha', inplace=True)
    df_grupos_pred.to_csv('Predicciones/predicciones_fase_grupos.csv',    index=False, encoding='utf-8-sig')
    clasif[['Grupo', 'Equipo', 'Pts', 'GF', 'GC', 'DG', 'Posicion']].to_csv(
        'Predicciones/clasificacion_grupos.csv', index=False, encoding='utf-8-sig')
    df_elim.to_csv('Predicciones/predicciones_eliminatorias.csv',         index=False, encoding='utf-8-sig')
    tabla_mc.to_csv('Predicciones/probabilidades_montecarlo.csv',          encoding='utf-8-sig')

    print(f"\n=== CAMPEÓN PREDICHO: {campeon} ===")
    print(f"\nTop 20 por probabilidad de campeón (Monte Carlo, {N_SIMULACIONES} sims):")
    print(tabla_mc.head(20).to_string())
    print("\nArchivos escritos en Predicciones/.")

    # ─────────────────────────────────────────────────────────────
    # NUEVO: IMPRESIÓN POR CONSOLA DE LA FASE DE GRUPOS
    # ─────────────────────────────────────────────────────────────
    print("\n" + "="*80)
    print("=== PREDICCIONES FASE DE GRUPOS (72 PARTIDOS) ===")
    print("="*80)
    # Formateamos el dataframe para que se vea limpio en consola
    columnas_a_mostrar = ['Grupo', 'Fecha', 'Local', 'Visitante', 'Marcador_Predicho', 'Prob_1', 'Prob_X', 'Prob_2']
    print(df_grupos_pred[columnas_a_mostrar].to_string(index=False))
