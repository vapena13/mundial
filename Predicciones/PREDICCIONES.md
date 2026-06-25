# 🏆 Predicción completa del Mundial 2026 — los 104 partidos

Generado con el modelo de este repositorio: regresores XGBoost (Tweedie) de goles + clasificador 1X2 XGBoost calibrado (sigmoid), modo de cancha `host-aware: cancha neutral salvo ventaja de anfitrión para EE. UU., México y Canadá`, temperatura `T=0.84` y simulación de **Monte Carlo de 5,000 mundiales** para las probabilidades por selección.

> Predicción generada el 2026-06-25, con histórico hasta 2026-05-29 y 52 resultado(s) real(es) fijado(s). La asignación de mejores terceros al cuadro usa la simplificación del notebook (ranking 1º-8º a huecos fijos), no la tabla oficial de la FIFA.

## Resumen

| | |
|---|---|
| 🥇 **Campeón predicho** | **🇫🇷 Francia** |
| 🥈 Subcampeón | 🇦🇷 Argentina |
| 🥉 Tercer puesto | 🇪🇸 España |

### Probabilidades de ser campeón (Top 10, Monte Carlo)

| # | Selección | Campeón | Final | Semis | Cuartos |
|---|---|---|---|---|---|
| 1 | 🇫🇷 Francia | **18.0%** | 27.0% | 41.8% | 51.0% |
| 2 | 🇦🇷 Argentina | **15.4%** | 29.1% | 47.2% | 65.1% |
| 3 | 🇪🇸 España | **12.9%** | 21.6% | 35.5% | 50.6% |
| 4 | 🇩🇪 Alemania | **9.5%** | 17.0% | 30.8% | 41.2% |
| 5 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | **8.6%** | 16.2% | 28.8% | 42.1% |
| 6 | 🇧🇪 Bélgica | **5.6%** | 11.8% | 25.1% | 45.9% |
| 7 | 🇭🇷 Croacia | **4.6%** | 9.1% | 18.8% | 29.8% |
| 8 | 🇵🇹 Portugal | **4.5%** | 8.9% | 16.8% | 31.7% |
| 9 | 🇧🇷 Brasil | **3.8%** | 9.6% | 20.1% | 37.8% |
| 10 | 🇲🇽 México | **3.1%** | 8.1% | 18.0% | 35.5% |

### Validación contra partidos jugados

| Métrica | Valor |
|---|---:|
| Partidos evaluados | 52 |
| Acierto 1X2 | 53.8% |
| Marcador exacto | 11.5% |
| Brier score 1X2 medio | 0.568 |
| Probabilidad media asignada al resultado real | 42.9% |

Detalle completo en [`Predicciones/VALIDACION.md`](VALIDACION.md) y [`Predicciones/validacion_predicciones.csv`](validacion_predicciones.csv).

## Fase de grupos — 72 partidos

Marcador = marcador exacto más probable según los goles esperados del modelo, condicionado al resultado 1X2 más probable.

### Grupo A

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-11 | 🇲🇽 México – 🇿🇦 Sudáfrica | **2-0** | 100% | 0% | 0% |
| 06-12 | 🇰🇷 Corea del Sur – 🇨🇿 República Checa | **2-1** | 100% | 0% | 0% |
| 06-18 | 🇨🇿 República Checa – 🇿🇦 Sudáfrica | **1-1** | 0% | 100% | 0% |
| 06-19 | 🇲🇽 México – 🇰🇷 Corea del Sur | **1-0** | 100% | 0% | 0% |
| 06-25 | 🇨🇿 República Checa – 🇲🇽 México | **0-3** | 0% | 0% | 100% |
| 06-25 | 🇿🇦 Sudáfrica – 🇰🇷 Corea del Sur | **1-0** | 100% | 0% | 0% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇲🇽 México ✅ | 9 | +6.00 |
| 2 | 🇿🇦 Sudáfrica ✅ | 4 | -1.00 |
| 3 | 🇰🇷 Corea del Sur 🟡 | 3 | -1.00 |
| 4 | 🇨🇿 República Checa | 1 | -4.00 |

### Grupo B

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-12 | 🇨🇦 Canadá – 🇧🇦 Bosnia-Herzegovina | **1-1** | 0% | 100% | 0% |
| 06-13 | 🇶🇦 Catar – 🇨🇭 Suiza | **1-1** | 0% | 100% | 0% |
| 06-18 | 🇨🇭 Suiza – 🇧🇦 Bosnia-Herzegovina | **4-1** | 100% | 0% | 0% |
| 06-19 | 🇨🇦 Canadá – 🇶🇦 Catar | **6-0** | 100% | 0% | 0% |
| 06-24 | 🇨🇭 Suiza – 🇨🇦 Canadá | **2-1** | 100% | 0% | 0% |
| 06-24 | 🇧🇦 Bosnia-Herzegovina – 🇶🇦 Catar | **3-1** | 100% | 0% | 0% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇨🇭 Suiza ✅ | 7 | +4.00 |
| 2 | 🇨🇦 Canadá ✅ | 4 | +5.00 |
| 3 | 🇧🇦 Bosnia-Herzegovina 🟡 | 4 | -1.00 |
| 4 | 🇶🇦 Catar | 1 | -8.00 |

### Grupo C

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-14 | 🇭🇹 Haití – 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia | **0-1** | 0% | 0% | 100% |
| 06-14 | 🇧🇷 Brasil – 🇲🇦 Marruecos | **1-1** | 0% | 100% | 0% |
| 06-20 | 🇧🇷 Brasil – 🇭🇹 Haití | **3-0** | 100% | 0% | 0% |
| 06-20 | 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia – 🇲🇦 Marruecos | **0-1** | 0% | 0% | 100% |
| 06-25 | 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia – 🇧🇷 Brasil | **0-3** | 0% | 0% | 100% |
| 06-25 | 🇲🇦 Marruecos – 🇭🇹 Haití | **4-2** | 100% | 0% | 0% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇧🇷 Brasil ✅ | 7 | +6.00 |
| 2 | 🇲🇦 Marruecos ✅ | 7 | +3.00 |
| 3 | 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia 🟡 | 3 | -3.00 |
| 4 | 🇭🇹 Haití | 0 | -6.00 |

### Grupo D

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-13 | 🇺🇸 EE. UU. – 🇵🇾 Paraguay | **4-1** | 100% | 0% | 0% |
| 06-14 | 🇦🇺 Australia – 🇹🇷 Turquía | **2-0** | 100% | 0% | 0% |
| 06-19 | 🇺🇸 EE. UU. – 🇦🇺 Australia | **2-0** | 100% | 0% | 0% |
| 06-20 | 🇹🇷 Turquía – 🇵🇾 Paraguay | **0-1** | 0% | 0% | 100% |
| 06-26 | 🇹🇷 Turquía – 🇺🇸 EE. UU. | **1-1** | 20% | 44% | 37% |
| 06-26 | 🇵🇾 Paraguay – 🇦🇺 Australia | **1-2** | 16% | 24% | 59% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇺🇸 EE. UU. ✅ | 7 | +5.38 |
| 2 | 🇦🇺 Australia ✅ | 6 | +0.36 |
| 3 | 🇵🇾 Paraguay 🟡 | 3 | -2.36 |
| 4 | 🇹🇷 Turquía | 1 | -3.38 |

### Grupo E

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-14 | 🇩🇪 Alemania – 🇨🇼 Curazao | **7-1** | 100% | 0% | 0% |
| 06-15 | 🇨🇮 Costa de Marfil – 🇪🇨 Ecuador | **1-0** | 100% | 0% | 0% |
| 06-20 | 🇩🇪 Alemania – 🇨🇮 Costa de Marfil | **2-1** | 100% | 0% | 0% |
| 06-21 | 🇪🇨 Ecuador – 🇨🇼 Curazao | **0-0** | 0% | 100% | 0% |
| 06-25 | 🇨🇼 Curazao – 🇨🇮 Costa de Marfil | **0-2** | 11% | 29% | 60% |
| 06-25 | 🇪🇨 Ecuador – 🇩🇪 Alemania | **0-2** | 13% | 34% | 53% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇩🇪 Alemania ✅ | 9 | +8.36 |
| 2 | 🇨🇮 Costa de Marfil ✅ | 6 | +1.62 |
| 3 | 🇪🇨 Ecuador 🟡 | 1 | -2.36 |
| 4 | 🇨🇼 Curazao | 1 | -7.62 |

### Grupo F

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-14 | 🇳🇱 Países Bajos – 🇯🇵 Japón | **2-2** | 0% | 100% | 0% |
| 06-15 | 🇸🇪 Suecia – 🇹🇳 Túnez | **5-1** | 100% | 0% | 0% |
| 06-20 | 🇳🇱 Países Bajos – 🇸🇪 Suecia | **5-1** | 100% | 0% | 0% |
| 06-21 | 🇹🇳 Túnez – 🇯🇵 Japón | **0-4** | 0% | 0% | 100% |
| 06-26 | 🇹🇳 Túnez – 🇳🇱 Países Bajos | **1-2** | 17% | 27% | 56% |
| 06-26 | 🇯🇵 Japón – 🇸🇪 Suecia | **2-1** | 56% | 27% | 17% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇳🇱 Países Bajos ✅ | 7 | +4.69 |
| 2 | 🇯🇵 Japón ✅ | 7 | +4.17 |
| 3 | 🇸🇪 Suecia 🟡 | 3 | -0.17 |
| 4 | 🇹🇳 Túnez | 0 | -8.69 |

### Grupo G

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-15 | 🇧🇪 Bélgica – 🇪🇬 Egipto | **1-1** | 0% | 100% | 0% |
| 06-16 | 🇮🇷 Irán – 🇳🇿 Nueva Zelanda | **2-2** | 0% | 100% | 0% |
| 06-21 | 🇧🇪 Bélgica – 🇮🇷 Irán | **0-0** | 0% | 100% | 0% |
| 06-22 | 🇳🇿 Nueva Zelanda – 🇪🇬 Egipto | **1-3** | 0% | 0% | 100% |
| 06-27 | 🇪🇬 Egipto – 🇮🇷 Irán | **0-1** | 16% | 35% | 49% |
| 06-27 | 🇳🇿 Nueva Zelanda – 🇧🇪 Bélgica | **0-3** | 10% | 22% | 69% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇧🇪 Bélgica ✅ | 5 | +1.92 |
| 2 | 🇮🇷 Irán ✅ | 5 | +0.32 |
| 3 | 🇪🇬 Egipto 🟡 | 4 | +1.68 |
| 4 | 🇳🇿 Nueva Zelanda | 1 | -3.92 |

### Grupo H

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-15 | 🇪🇸 España – 🇨🇻 Cabo Verde | **0-0** | 0% | 100% | 0% |
| 06-16 | 🇸🇦 Arabia Saudí – 🇺🇾 Uruguay | **1-1** | 0% | 100% | 0% |
| 06-21 | 🇪🇸 España – 🇸🇦 Arabia Saudí | **4-0** | 100% | 0% | 0% |
| 06-22 | 🇺🇾 Uruguay – 🇨🇻 Cabo Verde | **2-2** | 0% | 100% | 0% |
| 06-27 | 🇨🇻 Cabo Verde – 🇸🇦 Arabia Saudí | **0-1** | 32% | 34% | 34% |
| 06-27 | 🇺🇾 Uruguay – 🇪🇸 España | **0-2** | 19% | 31% | 50% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇪🇸 España ✅ | 7 | +5.08 |
| 2 | 🇸🇦 Arabia Saudí ✅ | 4 | -4.37 |
| 3 | 🇨🇻 Cabo Verde 🟡 | 2 | +0.37 |
| 4 | 🇺🇾 Uruguay | 2 | -1.08 |

### Grupo I

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-16 | 🇫🇷 Francia – 🇸🇳 Senegal | **3-1** | 100% | 0% | 0% |
| 06-17 | 🇮🇶 Irak – 🇳🇴 Noruega | **1-4** | 0% | 0% | 100% |
| 06-22 | 🇫🇷 Francia – 🇮🇶 Irak | **3-0** | 100% | 0% | 0% |
| 06-23 | 🇳🇴 Noruega – 🇸🇳 Senegal | **3-2** | 100% | 0% | 0% |
| 06-26 | 🇳🇴 Noruega – 🇫🇷 Francia | **1-3** | 9% | 25% | 66% |
| 06-26 | 🇸🇳 Senegal – 🇮🇶 Irak | **2-0** | 67% | 22% | 10% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇫🇷 Francia ✅ | 9 | +6.33 |
| 2 | 🇳🇴 Noruega ✅ | 6 | +2.67 |
| 3 | 🇸🇳 Senegal 🟡 | 3 | -1.41 |
| 4 | 🇮🇶 Irak | 0 | -7.59 |

### Grupo J

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-17 | 🇦🇷 Argentina – 🇩🇿 Argelia | **3-0** | 100% | 0% | 0% |
| 06-17 | 🇦🇹 Austria – 🇯🇴 Jordania | **3-1** | 100% | 0% | 0% |
| 06-22 | 🇦🇷 Argentina – 🇦🇹 Austria | **2-0** | 100% | 0% | 0% |
| 06-23 | 🇯🇴 Jordania – 🇩🇿 Argelia | **1-2** | 0% | 0% | 100% |
| 06-28 | 🇩🇿 Argelia – 🇦🇹 Austria | **1-2** | 30% | 29% | 41% |
| 06-28 | 🇯🇴 Jordania – 🇦🇷 Argentina | **0-4** | 6% | 16% | 78% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇦🇷 Argentina ✅ | 9 | +7.62 |
| 2 | 🇦🇹 Austria ✅ | 6 | +0.30 |
| 3 | 🇩🇿 Argelia 🟡 | 3 | -2.30 |
| 4 | 🇯🇴 Jordania | 0 | -5.62 |

### Grupo K

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-17 | 🇵🇹 Portugal – 🇨🇩 RD Congo | **1-1** | 0% | 100% | 0% |
| 06-18 | 🇺🇿 Uzbekistán – 🇨🇴 Colombia | **1-3** | 0% | 0% | 100% |
| 06-23 | 🇵🇹 Portugal – 🇺🇿 Uzbekistán | **4-0** | 62% | 26% | 11% |
| 06-24 | 🇨🇴 Colombia – 🇨🇩 RD Congo | **1-0** | 100% | 0% | 0% |
| 06-28 | 🇨🇩 RD Congo – 🇺🇿 Uzbekistán | **1-0** | 46% | 32% | 22% |
| 06-28 | 🇨🇴 Colombia – 🇵🇹 Portugal | **1-2** | 21% | 35% | 45% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇵🇹 Portugal ✅ | 7 | +3.51 |
| 2 | 🇨🇴 Colombia ✅ | 6 | +1.86 |
| 3 | 🇨🇩 RD Congo 🟡 | 4 | -0.41 |
| 4 | 🇺🇿 Uzbekistán | 0 | -4.96 |

### Grupo L

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-17 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra – 🇭🇷 Croacia | **4-2** | 100% | 0% | 0% |
| 06-18 | 🇬🇭 Ghana – 🇵🇦 Panamá | **1-0** | 100% | 0% | 0% |
| 06-23 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra – 🇬🇭 Ghana | **0-0** | 0% | 100% | 0% |
| 06-24 | 🇵🇦 Panamá – 🇭🇷 Croacia | **0-3** | 15% | 24% | 61% |
| 06-27 | 🇭🇷 Croacia – 🇬🇭 Ghana | **2-0** | 71% | 21% | 8% |
| 06-27 | 🇵🇦 Panamá – 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | **0-3** | 12% | 28% | 60% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra ✅ | 7 | +4.09 |
| 2 | 🇭🇷 Croacia ✅ | 6 | +1.00 |
| 3 | 🇬🇭 Ghana 🟡 | 4 | -0.38 |
| 4 | 🇵🇦 Panamá | 0 | -4.72 |

✅ clasificado directo · 🟡 tercero (pasan los 8 mejores)

## Eliminatorias — 32 partidos

Si el empate es el resultado más probable, el cruce se decide por penaltis a favor del equipo con mayor probabilidad de victoria.

### Dieciseisavos de final (16 cruces) · *28 jun - 3 jul*

| Cruce | Pred. | Avanza | P(1) | P(X) | P(2) |
|---|:-:|---|--:|--:|--:|
| 🇩🇪 Alemania – 🇪🇬 Egipto | **2-0** | **🇩🇪 Alemania** | 58% | 31% | 11% |
| 🇫🇷 Francia – 🇬🇭 Ghana | **3-0** | **🇫🇷 Francia** | 74% | 19% | 7% |
| 🇿🇦 Sudáfrica – 🇨🇦 Canadá | **1-1 (pen)** | **🇨🇦 Canadá** | 18% | 53% | 28% |
| 🇳🇱 Países Bajos – 🇲🇦 Marruecos | **2-1** | **🇳🇱 Países Bajos** | 54% | 26% | 19% |
| 🇨🇴 Colombia – 🇭🇷 Croacia | **1-2** | **🇭🇷 Croacia** | 15% | 32% | 53% |
| 🇪🇸 España – 🇦🇹 Austria | **2-1** | **🇪🇸 España** | 48% | 31% | 20% |
| 🇺🇸 EE. UU. – 🇨🇩 RD Congo | **2-0** | **🇺🇸 EE. UU.** | 59% | 26% | 15% |
| 🇧🇪 Bélgica – 🇧🇦 Bosnia-Herzegovina | **4-0** | **🇧🇪 Bélgica** | 68% | 20% | 12% |
| 🇧🇷 Brasil – 🇯🇵 Japón | **1-1 (pen)** | **🇧🇷 Brasil** | 34% | 43% | 23% |
| 🇨🇮 Costa de Marfil – 🇳🇴 Noruega | **2-1** | **🇨🇮 Costa de Marfil** | 53% | 28% | 19% |
| 🇲🇽 México – 🇸🇪 Suecia | **2-1** | **🇲🇽 México** | 58% | 26% | 16% |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra – 🇰🇷 Corea del Sur | **2-0** | **🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra** | 53% | 34% | 13% |
| 🇦🇷 Argentina – 🇸🇦 Arabia Saudí | **3-0** | **🇦🇷 Argentina** | 76% | 17% | 7% |
| 🇦🇺 Australia – 🇮🇷 Irán | **1-2** | **🇮🇷 Irán** | 16% | 30% | 55% |
| 🇨🇭 Suiza – 🇸🇳 Senegal | **1-2** | **🇸🇳 Senegal** | 21% | 33% | 46% |
| 🇵🇹 Portugal – 🇩🇿 Argelia | **2-1** | **🇵🇹 Portugal** | 48% | 30% | 22% |

### Octavos de final · *4 - 7 jul*

| Cruce | Pred. | Avanza | P(1) | P(X) | P(2) |
|---|:-:|---|--:|--:|--:|
| 🇩🇪 Alemania – 🇫🇷 Francia | **2-2 (pen)** | **🇫🇷 Francia** | 25% | 47% | 28% |
| 🇨🇦 Canadá – 🇳🇱 Países Bajos | **0-1** | **🇳🇱 Países Bajos** | 24% | 30% | 46% |
| 🇭🇷 Croacia – 🇪🇸 España | **1-2** | **🇪🇸 España** | 21% | 38% | 41% |
| 🇺🇸 EE. UU. – 🇧🇪 Bélgica | **1-2** | **🇧🇪 Bélgica** | 21% | 37% | 43% |
| 🇧🇷 Brasil – 🇨🇮 Costa de Marfil | **1-1 (pen)** | **🇧🇷 Brasil** | 31% | 42% | 28% |
| 🇲🇽 México – 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | **1-1 (pen)** | **🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra** | 29% | 38% | 32% |
| 🇦🇷 Argentina – 🇮🇷 Irán | **2-1** | **🇦🇷 Argentina** | 42% | 40% | 18% |
| 🇸🇳 Senegal – 🇵🇹 Portugal | **1-2** | **🇵🇹 Portugal** | 28% | 35% | 37% |

### Cuartos de final · *9 - 11 jul*

| Cruce | Pred. | Avanza | P(1) | P(X) | P(2) |
|---|:-:|---|--:|--:|--:|
| 🇫🇷 Francia – 🇳🇱 Países Bajos | **2-1** | **🇫🇷 Francia** | 52% | 32% | 16% |
| 🇪🇸 España – 🇧🇪 Bélgica | **2-1** | **🇪🇸 España** | 36% | 35% | 29% |
| 🇧🇷 Brasil – 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | **1-2** | **🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra** | 24% | 37% | 39% |
| 🇦🇷 Argentina – 🇵🇹 Portugal | **2-2 (pen)** | **🇦🇷 Argentina** | 36% | 44% | 20% |

### Semifinales · *14 - 15 jul*

| Cruce | Pred. | Avanza | P(1) | P(X) | P(2) |
|---|:-:|---|--:|--:|--:|
| 🇫🇷 Francia – 🇪🇸 España | **1-1 (pen)** | **🇫🇷 Francia** | 29% | 44% | 27% |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra – 🇦🇷 Argentina | **1-1 (pen)** | **🇦🇷 Argentina** | 25% | 44% | 31% |

### Partido por el 3er puesto · *18 jul*

| Cruce | Pred. | Avanza | P(1) | P(X) | P(2) |
|---|:-:|---|--:|--:|--:|
| 🇪🇸 España – 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | **1-1 (pen)** | **🇪🇸 España** | 37% | 39% | 24% |

### 🏆 Gran Final — MetLife Stadium, Nueva York/Nueva Jersey · *19 jul*

| Cruce | Pred. | Avanza | P(1) | P(X) | P(2) |
|---|:-:|---|--:|--:|--:|
| 🇫🇷 Francia – 🇦🇷 Argentina | **1-1 (pen)** | **🇫🇷 Francia** | 32% | 46% | 22% |

## Probabilidades por selección — 10.000 mundiales simulados

| Selección | Pasa grupos | Octavos | Cuartos | Semis | Final | 🏆 Campeón |
|---|--:|--:|--:|--:|--:|--:|
| 🇫🇷 Francia | 100.0% | 85.2% | 51.0% | 41.8% | 27.0% | **18.0%** |
| 🇦🇷 Argentina | 100.0% | 84.3% | 65.1% | 47.2% | 29.1% | **15.4%** |
| 🇪🇸 España | 100.0% | 70.2% | 50.6% | 35.5% | 21.6% | **12.9%** |
| 🇩🇪 Alemania | 100.0% | 77.6% | 41.2% | 30.8% | 17.0% | **9.5%** |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | 100.0% | 73.9% | 42.1% | 28.8% | 16.2% | **8.6%** |
| 🇧🇪 Bélgica | 90.4% | 70.9% | 45.9% | 25.1% | 11.8% | **5.6%** |
| 🇭🇷 Croacia | 84.1% | 51.3% | 29.8% | 18.8% | 9.1% | **4.6%** |
| 🇵🇹 Portugal | 90.9% | 59.6% | 31.7% | 16.8% | 8.9% | **4.5%** |
| 🇧🇷 Brasil | 100.0% | 64.1% | 37.8% | 20.1% | 9.6% | **3.8%** |
| 🇲🇽 México | 100.0% | 70.3% | 35.5% | 18.0% | 8.1% | **3.1%** |
| 🇨🇮 Costa de Marfil | 98.5% | 67.2% | 34.3% | 14.6% | 6.6% | **2.7%** |
| 🇸🇳 Senegal | 46.3% | 28.8% | 19.5% | 10.2% | 5.1% | **1.9%** |
| 🇳🇱 Países Bajos | 100.0% | 58.1% | 35.8% | 11.0% | 4.4% | **1.9%** |
| 🇯🇵 Japón | 100.0% | 41.4% | 21.7% | 7.5% | 3.0% | **1.2%** |
| 🇨🇴 Colombia | 100.0% | 53.3% | 23.5% | 8.9% | 3.0% | **1.0%** |
| 🇮🇷 Irán | 84.8% | 51.0% | 20.6% | 7.4% | 3.0% | **1.0%** |
| 🇨🇭 Suiza | 100.0% | 55.1% | 25.9% | 8.3% | 2.9% | **0.8%** |
| 🇺🇾 Uruguay | 45.1% | 22.1% | 10.4% | 4.6% | 1.8% | **0.6%** |
| 🇦🇹 Austria | 99.9% | 33.8% | 12.2% | 4.8% | 1.7% | **0.6%** |
| 🇺🇸 EE. UU. | 100.0% | 69.3% | 31.3% | 8.4% | 2.0% | **0.5%** |
| 🇲🇦 Marruecos | 100.0% | 35.5% | 21.4% | 5.5% | 1.6% | **0.5%** |
| 🇨🇦 Canadá | 100.0% | 61.0% | 22.6% | 4.2% | 1.4% | **0.3%** |
| 🇩🇿 Argelia | 86.0% | 29.1% | 12.1% | 3.7% | 1.0% | **0.2%** |
| 🇳🇴 Noruega | 100.0% | 35.1% | 10.3% | 3.0% | 0.8% | **0.2%** |
| 🇰🇷 Corea del Sur | 95.1% | 34.0% | 12.7% | 3.8% | 0.9% | **0.2%** |
| 🇿🇦 Sudáfrica | 100.0% | 39.0% | 14.2% | 2.2% | 0.6% | **0.1%** |
| 🇪🇬 Egipto | 100.0% | 42.3% | 10.0% | 2.3% | 0.4% | **0.1%** |
| 🇦🇺 Australia | 100.0% | 28.6% | 4.8% | 1.1% | 0.2% | **0.1%** |
| 🇧🇦 Bosnia-Herzegovina | 100.0% | 18.8% | 4.5% | 1.0% | 0.2% | **0.1%** |
| 🇸🇪 Suecia | 99.8% | 24.4% | 7.4% | 1.7% | 0.3% | **0.0%** |
| 🇨🇻 Cabo Verde | 66.7% | 9.2% | 2.7% | 0.7% | 0.1% | **0.0%** |
| 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia | 13.3% | 3.4% | 1.5% | 0.2% | 0.1% | **0.0%** |
| 🇨🇩 RD Congo | 45.8% | 8.5% | 2.5% | 0.6% | 0.0% | **0.0%** |
| 🇬🇭 Ghana | 100.0% | 17.6% | 2.4% | 0.4% | 0.0% | **0.0%** |
| 🇵🇾 Paraguay | 66.3% | 10.1% | 2.0% | 0.3% | 0.0% | **0.0%** |
| 🇪🇨 Ecuador | 13.8% | 4.5% | 1.6% | 0.3% | 0.0% | **0.0%** |
| 🇵🇦 Panamá | 6.9% | 1.2% | 0.3% | 0.1% | 0.0% | **0.0%** |
| 🇺🇿 Uzbekistán | 12.4% | 2.6% | 0.3% | 0.1% | 0.0% | **0.0%** |
| 🇸🇦 Arabia Saudí | 33.4% | 3.1% | 0.5% | 0.1% | 0.0% | **0.0%** |
| 🇳🇿 Nueva Zelanda | 9.6% | 2.9% | 0.4% | 0.0% | 0.0% | **0.0%** |
| 🇨🇼 Curazao | 10.4% | 1.5% | 0.2% | 0.0% | 0.0% | **0.0%** |
| 🇶🇦 Catar | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| 🇭🇹 Haití | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| 🇮🇶 Irak | 0.3% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| 🇯🇴 Jordania | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| 🇨🇿 República Checa | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| 🇹🇷 Turquía | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| 🇹🇳 Túnez | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |

## Validación con los partidos ya jugados

| Partido | Predicción del modelo | Resultado real |
|---|:-:|:-:|
| 🇲🇽 México – 🇿🇦 Sudáfrica | 2-0 (P1 100%) | 2-0 ✅ ganador acertado |
| 🇰🇷 Corea del Sur – 🇨🇿 República Checa | 2-1 (P1 100%) | 2-1 ✅ ganador acertado |

---
*Predicciones generadas automáticamente con `prediccion_mundial.py`. El fútbol, por suerte, no entiende de modelos.* ⚽