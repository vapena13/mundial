# Validacion de predicciones vs resultados reales

Compara la prediccion previa del modelo contra los partidos ya jugados. Los partidos jugados se fijan despues para tablas y Monte Carlo, pero aqui se evalua lo que el modelo habia dicho antes de conocer el marcador real.

## Resumen

| Metrica | Valor |
|---|---:|
| Partidos evaluados | 52 |
| Acierto 1X2 | 53.8% |
| Marcador exacto | 11.5% |
| Error medio de goles totales | 2.00 |
| Brier score 1X2 medio | 0.568 |
| Probabilidad media asignada al resultado real | 42.9% |

## Mayores sorpresas

| Fecha | Partido | Prediccion previa | Real | Prob. real previa |
|---|---|---:|---:|---:|
| 2026-06-20 | Turquía - Paraguay | 1-0 (1) | 0-1 (2) | 13.1% |
| 2026-06-23 | Inglaterra - Ghana | 2-0 (1) | 0-0 (X) | 18.4% |
| 2026-06-23 | Noruega - Senegal | 0-2 (2) | 3-2 (1) | 18.8% |
| 2026-06-25 | Sudáfrica - Corea del Sur | 1-1 (X) | 1-0 (1) | 21.3% |
| 2026-06-16 | Arabia Saudí - Uruguay | 0-2 (2) | 1-1 (X) | 21.5% |
| 2026-06-14 | Australia - Turquía | 1-2 (2) | 2-0 (1) | 21.9% |
| 2026-06-22 | Uruguay - Cabo Verde | 1-0 (1) | 2-2 (X) | 24.1% |
| 2026-06-11 | México - Sudáfrica | 1-1 (X) | 2-0 (1) | 24.1% |
| 2026-06-15 | España - Cabo Verde | 2-0 (1) | 0-0 (X) | 24.9% |
| 2026-06-16 | Irán - Nueva Zelanda | 2-0 (1) | 2-2 (X) | 25.6% |

## Detalle

| Fecha | Grupo | Partido | Pred. previa | Real | Acierto 1X2 | Prob. real previa | Brier |
|---|---|---|---:|---:|:-:|---:|---:|
| 2026-06-11 | A | México - Sudáfrica | 1-1 | 2-0 | no | 24.1% | 0.975 |
| 2026-06-12 | A | Corea del Sur - República Checa | 2-1 | 2-1 | si | 50.3% | 0.375 |
| 2026-06-12 | B | Canadá - Bosnia-Herzegovina | 2-0 | 1-1 | no | 35.1% | 0.670 |
| 2026-06-13 | B | Catar - Suiza | 1-2 | 1-1 | no | 32.9% | 0.710 |
| 2026-06-13 | D | EE. UU. - Paraguay | 2-0 | 4-1 | si | 67.4% | 0.172 |
| 2026-06-14 | C | Brasil - Marruecos | 2-1 | 1-1 | no | 30.5% | 0.758 |
| 2026-06-14 | C | Haití - Escocia | 0-2 | 0-1 | si | 51.7% | 0.356 |
| 2026-06-14 | D | Australia - Turquía | 1-2 | 2-0 | no | 21.9% | 0.958 |
| 2026-06-14 | E | Alemania - Curazao | 3-0 | 7-1 | si | 72.8% | 0.118 |
| 2026-06-14 | F | Países Bajos - Japón | 1-1 | 2-2 | si | 38.8% | 0.565 |
| 2026-06-15 | E | Costa de Marfil - Ecuador | 1-0 | 1-0 | si | 51.9% | 0.356 |
| 2026-06-15 | F | Suecia - Túnez | 2-1 | 5-1 | si | 40.6% | 0.530 |
| 2026-06-15 | G | Bélgica - Egipto | 2-0 | 1-1 | no | 26.5% | 0.934 |
| 2026-06-15 | H | España - Cabo Verde | 2-0 | 0-0 | no | 24.9% | 0.980 |
| 2026-06-16 | G | Irán - Nueva Zelanda | 2-0 | 2-2 | no | 25.6% | 0.970 |
| 2026-06-16 | H | Arabia Saudí - Uruguay | 0-2 | 1-1 | no | 21.5% | 1.098 |
| 2026-06-16 | I | Francia - Senegal | 1-1 | 3-1 | no | 37.4% | 0.605 |
| 2026-06-17 | I | Irak - Noruega | 0-2 | 1-4 | si | 58.0% | 0.266 |
| 2026-06-17 | J | Argentina - Argelia | 1-0 | 3-0 | si | 56.5% | 0.291 |
| 2026-06-17 | J | Austria - Jordania | 3-0 | 3-1 | si | 71.7% | 0.126 |
| 2026-06-17 | K | Portugal - RD Congo | 2-0 | 1-1 | no | 26.7% | 0.922 |
| 2026-06-17 | L | Inglaterra - Croacia | 1-1 | 4-2 | no | 36.3% | 0.623 |
| 2026-06-18 | A | República Checa - Sudáfrica | 1-1 | 1-1 | si | 38.8% | 0.564 |
| 2026-06-18 | B | Suiza - Bosnia-Herzegovina | 2-1 | 4-1 | si | 43.7% | 0.476 |
| 2026-06-18 | K | Uzbekistán - Colombia | 0-2 | 1-3 | si | 59.9% | 0.250 |
| 2026-06-18 | L | Ghana - Panamá | 0-1 | 1-0 | no | 30.1% | 0.735 |
| 2026-06-19 | A | México - Corea del Sur | 1-1 | 1-0 | no | 32.1% | 0.726 |
| 2026-06-19 | B | Canadá - Catar | 0-1 | 6-0 | no | 29.1% | 0.757 |
| 2026-06-19 | D | EE. UU. - Australia | 1-0 | 2-0 | si | 55.6% | 0.308 |
| 2026-06-20 | C | Escocia - Marruecos | 1-2 | 0-1 | si | 46.5% | 0.435 |
| 2026-06-20 | C | Brasil - Haití | 3-0 | 3-0 | si | 70.2% | 0.141 |
| 2026-06-20 | D | Turquía - Paraguay | 1-0 | 0-1 | no | 13.1% | 1.224 |
| 2026-06-20 | E | Alemania - Costa de Marfil | 1-1 | 2-1 | no | 31.1% | 0.750 |
| 2026-06-20 | F | Países Bajos - Suecia | 2-1 | 5-1 | si | 59.1% | 0.255 |
| 2026-06-21 | E | Ecuador - Curazao | 2-0 | 0-0 | no | 29.7% | 0.828 |
| 2026-06-21 | F | Túnez - Japón | 0-1 | 0-4 | si | 55.8% | 0.304 |
| 2026-06-21 | G | Bélgica - Irán | 2-0 | 0-0 | no | 32.5% | 0.715 |
| 2026-06-21 | H | España - Arabia Saudí | 2-0 | 4-0 | si | 67.9% | 0.166 |
| 2026-06-22 | G | Nueva Zelanda - Egipto | 0-1 | 1-3 | si | 49.5% | 0.391 |
| 2026-06-22 | H | Uruguay - Cabo Verde | 1-0 | 2-2 | no | 24.1% | 0.966 |
| 2026-06-22 | I | Francia - Irak | 3-0 | 3-0 | si | 73.4% | 0.113 |
| 2026-06-22 | J | Argentina - Austria | 2-1 | 2-0 | si | 45.7% | 0.451 |
| 2026-06-23 | I | Noruega - Senegal | 0-2 | 3-2 | no | 18.8% | 1.012 |
| 2026-06-23 | J | Jordania - Argelia | 0-2 | 1-2 | si | 69.6% | 0.143 |
| 2026-06-23 | L | Inglaterra - Ghana | 2-0 | 0-0 | no | 18.4% | 1.215 |
| 2026-06-24 | B | Bosnia-Herzegovina - Catar | 1-2 | 3-1 | no | 28.9% | 0.759 |
| 2026-06-24 | B | Suiza - Canadá | 1-0 | 2-1 | si | 37.8% | 0.581 |
| 2026-06-24 | K | Colombia - RD Congo | 1-0 | 1-0 | si | 49.7% | 0.386 |
| 2026-06-25 | A | Sudáfrica - Corea del Sur | 1-1 | 1-0 | no | 21.3% | 0.943 |
| 2026-06-25 | A | República Checa - México | 1-2 | 0-3 | si | 65.1% | 0.193 |
| 2026-06-25 | C | Marruecos - Haití | 2-0 | 4-2 | si | 66.1% | 0.178 |
| 2026-06-25 | C | Escocia - Brasil | 1-2 | 0-3 | si | 64.6% | 0.198 |
