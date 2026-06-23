# Ejecucion en Colab gratuito (CPU)

El perfil `colab` limita el paralelismo a dos CPU, usa arboles `hist`, reduce la
busqueda de hiperparametros y conserva 5.000 simulaciones Monte Carlo. El modo
completo original sigue disponible con `--profile full`.

## Ejecucion

```bash
pip install -r requirements-colab.txt
python 04_Prediccion/prediccion_mundial.py --profile colab
python 04_Prediccion/generar_informe.py
python 05_Web/generar_web.py
```

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
