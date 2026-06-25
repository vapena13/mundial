# Simulaciones Mundial 2026 ⚽🏆

¿Quién va a ganar el Mundial 2026? Este repositorio responde con datos: scrapea histórico de estadísticas de selecciones, entrena modelos XGBoost y simula miles de mundiales con Monte Carlo para estimar el rendimiento esperado de cada selección, hasta predecir los 104 partidos del torneo.

Esta versión está adaptada para correr en **Google Colab gratuito (CPU)**, permite fijar resultados reales conforme se juegan los partidos y usa un tratamiento de cancha `host-aware`: sede neutral para casi todos los partidos, con ventaja de anfitrión solo cuando juegan **EE. UU., México o Canadá**.

---

## 🔄 El pipeline, paso a paso

### 1️⃣ Scraping — [`01_Scraping/`](01_Scraping/)
Un scraper (Selenium + BeautifulSoup) se descarga **todo el histórico de estadísticas de FlashScore**: resultados, xG, posesión, remates a puerta, córneres, faltas, paradas, pases... de los últimos partidos de cada selección, más el ranking FIFA. Si no quieres scrapear desde cero, los datos ya descargados están en [`Data/`](Data/).

### 2️⃣ Limpieza de datos — [`02_Limpieza_Datos/`](02_Limpieza_Datos/)
El notebook `Data Cleaning.ipynb` hace el JOIN de las distintas fuentes descargadas y una buena limpieza para **pasar del HTML scrapeado en bruto a un dataset modelable**: una fila por partido con las estadísticas de los dos equipos.

### 3️⃣ Ingeniería de variables
Sobre los datos limpios se construyen **medias móviles (últimos 5 partidos e histórico), ratios y diferencias** entre equipos para capturar el *estado de forma* de cada selección justo antes del partido: diferencia de puntos Elo/FIFA, probabilidad implícita del Elo, tiers de nivel, pesos por confederación y diferenciales de cada estadística. Eso es lo que el modelo "ve" para predecir el resultado.

### 4️⃣ Dos modelos XGBoost — [`03_Modelado_Simulacion/`](03_Modelado_Simulacion/)
Con los datos listos, en `Modelling.ipynb` se entrenan dos modelos:

1. **Modelo de goles**: dos regresores XGBoost con objetivo Tweedie (a medio camino entre Poisson y Gamma, ideal para fútbol) que predicen los goles esperados de cada equipo.
2. **Modelo de resultado**: un clasificador XGBoost 1X2 que usa como meta-variables las predicciones de goles del primero, con **probabilidades calibradas** (calibración isotónica) y validación temporal para no mezclar pasado y futuro.

### 5️⃣ El comportamiento estocástico: Monte Carlo
¿Por qué no basta con simular un mundial? Porque la realidad es **estocástica**. Si solo simulásemos uno, una selección con el 51% de probabilidades de pasar, pasaría exactamente igual que una con el 99%. Para capturar el efecto de la varianza, simulamos miles de mundiales diferentes. En el perfil `colab` se usan **5.000 simulaciones**; el modo completo puede subir ese número.

### 🌐 Web de predicciones diarias — [`05_Web/`](05_Web/) → [`docs/`](docs/)
Una página estática (lista para **GitHub Pages**) con las predicciones de cada día: probabilidades de victoria calibradas, córners esperados (líneas 7.5/8.5/9.5), tarjetas esperadas (líneas 3.5/4.5), marcador más probable, tabla de campeón por Monte Carlo y el cuadro completo de eliminatorias. La sección «Partidos de hoy» se calcula con la fecha local del visitante, así que **se actualiza sola cada día** sin regenerar nada; además, un workflow de GitHub Actions ([`.github/workflows/actualizar_web.yml`](.github/workflows/actualizar_web.yml)) la regenera a diario por si cambian los datos.

Para activarla en este repo: en GitHub ve a **Settings → Pages → Build and deployment → Source: Deploy from a branch → Branch: `main` → Folder: `/docs` → Save**. La web quedará en:

`https://vapena13.github.io/mundial/`

### 6️⃣ Predicción de los 104 partidos — [`04_Prediccion/`](04_Prediccion/) → [`Predicciones/`](Predicciones/)
`prediccion_mundial.py` es el pipeline completo en un script: entrena los modelos (si no existen los `.pkl`), predice los 72 partidos de la fase de grupos, construye el cuadro completo de eliminatorias con el resultado más probable de cada cruce (incluido el 3er puesto) y corre el Monte Carlo. `generar_informe.py` lo convierte en un informe legible.

**Resultados** en [`Predicciones/PREDICCIONES.md`](Predicciones/PREDICCIONES.md): marcador más probable y probabilidades 1X2 de los 104 partidos, clasificaciones de los 12 grupos, cuadro hasta la final y probabilidades de campeón por selección (los mismos datos en CSV en la misma carpeta).

### 7️⃣ Actualización con resultados reales
Los marcadores ya jugados se guardan en [`Data/resultados_reales.csv`](Data/resultados_reales.csv). Cada fila fija un partido en fase de grupos y el modelo recalcula tablas, cruces y Monte Carlo con ese resultado como hecho real. Las predicciones no se reentrenan con esa muestra pequeña; solo se actualiza la simulación del torneo.

Para no subestimar goles cuando el torneo real viene más abierto que el histórico, el pipeline calcula un `factor de goles` con los partidos ya jugados: compara goles reales contra xG previo del modelo y escala los xG de partidos pendientes y cruces. El ajuste queda acotado entre `0.85` y `1.35` para evitar sobrecorregir por pocos partidos.

Si además quieres que el modelo use las estadísticas reales recientes del mes
(xG, remates, córners, tarjetas, etc.), hay un flujo incremental:

```bash
pip install -r requirements-scraping.txt

# 1. Guardar URLs nuevas de Flashscore en un TXT, una por línea.
# 2. Abrir Chrome con depuración remota en el puerto 9222.
python 01_Scraping/scrapear_incremental.py --urls Data/urls_incremental_junio.txt

# 3. Regenerar features usando partidos jugados hasta la fecha elegida.
python 02_Limpieza_Datos/Data_Cleaning.py --features-hasta 2026-06-25

# 4. Reentrenar y regenerar predicciones.
python 04_Prediccion/prediccion_mundial.py --profile colab --venue-mode host-aware --force-retrain
python 04_Prediccion/generar_informe.py
python 05_Web/generar_web.py
```

Ese modo actualiza `datos_mundial.csv` con la forma más reciente por selección sin
romper el calendario de `partidos_mundial.csv`.

Además, el pipeline compara la predicción previa contra el marcador real y genera:

- [`Predicciones/VALIDACION.md`](Predicciones/VALIDACION.md): resumen legible de aciertos, errores y sorpresas.
- [`Predicciones/validacion_predicciones.csv`](Predicciones/validacion_predicciones.csv): detalle partido por partido para analizar la calibración.

---

## 📂 Estructura del repositorio

```
├── 01_Scraping/              # Extracción de datos de FlashScore (Selenium)
│   └── Scrapper.py
├── 02_Limpieza_Datos/        # JOIN y limpieza → dataset modelable
│   └── Data Cleaning.ipynb
├── 03_Modelado_Simulacion/   # Ingeniería de variables, XGBoost y Monte Carlo
│   └── Modelling.ipynb
├── 04_Prediccion/            # Pipeline end-to-end en script
│   ├── prediccion_mundial.py
│   └── generar_informe.py
├── 05_Web/                   # Generador de la web de predicciones diarias
│   └── generar_web.py
├── docs/                     # Web estática (GitHub Pages)
│   └── index.html
├── Data/                     # Datos scrapeados y procesados (CSV)
└── Predicciones/             # Predicción de los 104 partidos + Monte Carlo
    └── PREDICCIONES.md
```

## 🚀 Replicarlo

```bash
pip install pandas numpy xgboost scikit-learn joblib tqdm

# (Opcional) actualizar los datos desde cero
python 01_Scraping/Scrapper.py

# Limpieza y modelado explicados paso a paso: notebooks 02 y 03

# Predicción completa del Mundial en CPU/Colab
python 04_Prediccion/prediccion_mundial.py --profile colab --venue-mode host-aware
python 04_Prediccion/generar_informe.py

# Web de predicciones diarias (docs/index.html)
python 05_Web/generar_web.py
```

Para comparar supuestos de cancha:

```bash
python 04_Prediccion/prediccion_mundial.py --profile colab --venue-mode neutral
python 04_Prediccion/prediccion_mundial.py --profile colab --venue-mode host-aware
python 04_Prediccion/prediccion_mundial.py --profile colab --venue-mode listed
```

El CSV [`Predicciones/comparacion_modos_cancha.csv`](Predicciones/comparacion_modos_cancha.csv) muestra cómo cambian las probabilidades entre esos modos.

## 💡 Inspírate

Aprovecha este proyecto para hacer algo aún más profundo a partir de él: incorporar más datos, probar otros modelos u otros enfoques para la modelización y la simulación. Estaré encantado de que me cuentes lo que has construido en `@jyts__`.
