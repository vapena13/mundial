# Ejecucion en Colab gratuito (CPU)

El perfil `colab` limita el paralelismo a dos CPU, usa arboles `hist`, reduce la
busqueda de hiperparametros y conserva 5.000 simulaciones Monte Carlo. El modo
completo original sigue disponible con `--profile full`.

## Ejecucion

```bash
pip install -r requirements-colab.txt
python 04_Prediccion/prediccion_mundial.py --profile colab --venue-mode host-aware
python 04_Prediccion/generar_informe.py
python 05_Web/generar_web.py
```

Por defecto se usa `--venue-mode host-aware`: cancha neutral para casi todos los
partidos y ventaja de anfitrion solo cuando juega `EE. UU.`, `Mexico` o
`Canada`. Para comparar supuestos:

```bash
python 04_Prediccion/prediccion_mundial.py --profile colab --venue-mode neutral
python 04_Prediccion/prediccion_mundial.py --profile colab --venue-mode host-aware
python 04_Prediccion/prediccion_mundial.py --profile colab --venue-mode listed
```

El archivo `Predicciones/comparacion_modos_cancha.csv` muestra cuanto cambia la
probabilidad entre neutral puro y anfitrion-aware.

Cada corrida tambien genera:

- `Predicciones/VALIDACION.md`: resumen de acierto 1X2, marcador exacto,
  Brier score y mayores sorpresas.
- `Predicciones/validacion_predicciones.csv`: detalle partido por partido.

Si la consola muestra algo como `Factor goles=1.15`, significa que los goles
reales vienen 15% por encima del xG previo del modelo. Ese factor se aplica a
partidos pendientes y cruces para evitar marcadores demasiado conservadores.

## Estadisticas recientes de junio

El ajuste anterior corrige goles esperados, pero no actualiza xG, remates,
corners o tarjetas. Para eso hay que scrapear las estadisticas reales recientes:

```bash
pip install -r requirements-scraping.txt
python 01_Scraping/scrapear_incremental.py --urls Data/urls_incremental_junio.txt
python 02_Limpieza_Datos/Data_Cleaning.py --features-hasta 2026-06-25
python 04_Prediccion/prediccion_mundial.py --profile colab --venue-mode host-aware --force-retrain
python 04_Prediccion/generar_informe.py
python 05_Web/generar_web.py
```

`Data/urls_incremental_junio.txt` debe contener una URL de Flashscore por linea.
El scraper incremental agrega esas filas a `Data/partidos.csv` y evita duplicados.

Para una comprobacion rapida del pipeline:

```bash
python 04_Prediccion/prediccion_mundial.py --profile test --force-retrain
```

## Resultados ya jugados

Complete `Data/resultados_reales.csv` sin cambiar los nombres del calendario:

```csv
Equipo_Local,Equipo_Visitante,Goles_Local,Goles_Visitante
México,Sudáfrica,1,0
```

Los ejemplos anteriores son solo de formato. Deben usarse los nombres exactos
que aparecen en `Data/partidos_mundial.csv`. Un partido incluido queda fijado en
la tabla y en todas las simulaciones; no se usa esa muestra pequena para volver
a entrenar el modelo.

Los archivos `.pkl` se reutilizan automaticamente. Guardarlos en Google Drive
evita entrenar de nuevo cuando Colab elimina la sesion.

El paquete preparado incluye modelos entrenados con el perfil `colab`. Para
entrenarlos de nuevo desde cero use `--force-retrain`; sin esa opcion, actualizar
`resultados_reales.csv` solo recalcula tablas, cruces y simulaciones.

## Publicar la pagina web

El archivo visible es `docs/index.html`. Para verlo desde otro dispositivo:

1. Suba los cambios al repo `vapena13/mundial`.
2. En GitHub abra **Settings -> Pages**.
3. En **Build and deployment**, elija **Deploy from a branch**.
4. Seleccione branch `main` y carpeta `/docs`.
5. Guarde. Despues de unos minutos la pagina queda en:

```text
https://vapena13.github.io/mundial/
```

Cada vez que cambie `Data/resultados_reales.csv`, vuelva a correr los tres
comandos de ejecucion y suba los cambios de `Data/`, `Predicciones/` y `docs/`.
La validacion se recalcula con los partidos jugados que existan en ese CSV.
