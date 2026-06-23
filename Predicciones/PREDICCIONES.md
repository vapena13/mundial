# 🏆 Predicción completa del Mundial 2026 — los 104 partidos

Generado con el modelo de este repositorio: regresores XGBoost (Tweedie) de goles + clasificador 1X2 XGBoost calibrado (sigmoid), modo de cancha `host-aware: cancha neutral salvo ventaja de anfitrión para EE. UU., México y Canadá`, temperatura `T=0.84` y simulación de **Monte Carlo de 5,000 mundiales** para las probabilidades por selección.

> Predicción generada el 2026-06-23, con histórico hasta 2026-05-29 y 44 resultado(s) real(es) fijado(s). La asignación de mejores terceros al cuadro usa la simplificación del notebook (ranking 1º-8º a huecos fijos), no la tabla oficial de la FIFA.

## Resumen

| | |
|---|---|
| 🥇 **Campeón predicho** | **🇫🇷 Francia** |
| 🥈 Subcampeón | 🇦🇷 Argentina |
| 🥉 Tercer puesto | 🇪🇸 España |

### Probabilidades de ser campeón (Top 10, Monte Carlo)

| # | Selección | Campeón | Final | Semis | Cuartos |
|---|---|---|---|---|---|
| 1 | 🇫🇷 Francia | **17.2%** | 25.9% | 40.5% | 50.7% |
| 2 | 🇦🇷 Argentina | **14.5%** | 26.6% | 43.2% | 60.1% |
| 3 | 🇪🇸 España | **13.1%** | 21.9% | 36.0% | 49.5% |
| 4 | 🇩🇪 Alemania | **9.4%** | 16.9% | 29.7% | 40.0% |
| 5 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | **9.3%** | 17.7% | 31.4% | 45.4% |
| 6 | 🇧🇪 Bélgica | **5.3%** | 11.9% | 24.8% | 42.9% |
| 7 | 🇭🇷 Croacia | **5.1%** | 10.3% | 21.1% | 31.6% |
| 8 | 🇵🇹 Portugal | **4.8%** | 9.7% | 18.6% | 37.5% |
| 9 | 🇧🇷 Brasil | **4.1%** | 9.0% | 18.1% | 37.3% |
| 10 | 🇲🇽 México | **3.4%** | 9.0% | 19.5% | 37.5% |

## Fase de grupos — 72 partidos

Marcador = marcador exacto más probable según los goles esperados del modelo, condicionado al resultado 1X2 más probable.

### Grupo A

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-11 | 🇲🇽 México – 🇿🇦 Sudáfrica | **2-0** | 100% | 0% | 0% |
| 06-12 | 🇰🇷 Corea del Sur – 🇨🇿 República Checa | **2-1** | 100% | 0% | 0% |
| 06-18 | 🇨🇿 República Checa – 🇿🇦 Sudáfrica | **1-1** | 0% | 100% | 0% |
| 06-19 | 🇲🇽 México – 🇰🇷 Corea del Sur | **1-0** | 100% | 0% | 0% |
| 06-25 | 🇨🇿 República Checa – 🇲🇽 México | **1-2** | 10% | 25% | 65% |
| 06-25 | 🇿🇦 Sudáfrica – 🇰🇷 Corea del Sur | **1-1** | 21% | 48% | 31% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇲🇽 México ✅ | 9 | +3.91 |
| 2 | 🇰🇷 Corea del Sur ✅ | 4 | +0.16 |
| 3 | 🇿🇦 Sudáfrica 🟡 | 2 | -2.16 |
| 4 | 🇨🇿 República Checa | 1 | -1.91 |

### Grupo B

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-12 | 🇨🇦 Canadá – 🇧🇦 Bosnia-Herzegovina | **1-1** | 0% | 100% | 0% |
| 06-13 | 🇶🇦 Catar – 🇨🇭 Suiza | **1-1** | 0% | 100% | 0% |
| 06-18 | 🇨🇭 Suiza – 🇧🇦 Bosnia-Herzegovina | **4-1** | 100% | 0% | 0% |
| 06-19 | 🇨🇦 Canadá – 🇶🇦 Catar | **6-0** | 100% | 0% | 0% |
| 06-24 | 🇨🇭 Suiza – 🇨🇦 Canadá | **1-0** | 38% | 32% | 30% |
| 06-24 | 🇧🇦 Bosnia-Herzegovina – 🇶🇦 Catar | **1-2** | 29% | 34% | 38% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇨🇭 Suiza ✅ | 7 | +3.51 |
| 2 | 🇨🇦 Canadá ✅ | 4 | +5.49 |
| 3 | 🇶🇦 Catar 🟡 | 4 | -6.21 |
| 4 | 🇧🇦 Bosnia-Herzegovina | 1 | -2.79 |

### Grupo C

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-14 | 🇭🇹 Haití – 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia | **0-1** | 0% | 0% | 100% |
| 06-14 | 🇧🇷 Brasil – 🇲🇦 Marruecos | **1-1** | 0% | 100% | 0% |
| 06-20 | 🇧🇷 Brasil – 🇭🇹 Haití | **3-0** | 100% | 0% | 0% |
| 06-20 | 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia – 🇲🇦 Marruecos | **0-1** | 0% | 0% | 100% |
| 06-25 | 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia – 🇧🇷 Brasil | **1-2** | 11% | 25% | 65% |
| 06-25 | 🇲🇦 Marruecos – 🇭🇹 Haití | **2-0** | 66% | 22% | 12% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇧🇷 Brasil ✅ | 7 | +3.83 |
| 2 | 🇲🇦 Marruecos ✅ | 7 | +2.33 |
| 3 | 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia 🟡 | 3 | -0.83 |
| 4 | 🇭🇹 Haití | 0 | -5.33 |

### Grupo D

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-13 | 🇺🇸 EE. UU. – 🇵🇾 Paraguay | **4-1** | 100% | 0% | 0% |
| 06-14 | 🇦🇺 Australia – 🇹🇷 Turquía | **2-0** | 100% | 0% | 0% |
| 06-19 | 🇺🇸 EE. UU. – 🇦🇺 Australia | **2-0** | 100% | 0% | 0% |
| 06-20 | 🇹🇷 Turquía – 🇵🇾 Paraguay | **0-1** | 0% | 0% | 100% |
| 06-26 | 🇹🇷 Turquía – 🇺🇸 EE. UU. | **1-1** | 20% | 44% | 37% |
| 06-26 | 🇵🇾 Paraguay – 🇦🇺 Australia | **0-1** | 16% | 24% | 59% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇺🇸 EE. UU. ✅ | 7 | +5.33 |
| 2 | 🇦🇺 Australia ✅ | 6 | +0.31 |
| 3 | 🇵🇾 Paraguay 🟡 | 3 | -2.31 |
| 4 | 🇹🇷 Turquía | 1 | -3.33 |

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
| 1 | 🇩🇪 Alemania ✅ | 9 | +8.18 |
| 2 | 🇨🇮 Costa de Marfil ✅ | 6 | +1.41 |
| 3 | 🇪🇨 Ecuador 🟡 | 1 | -2.18 |
| 4 | 🇨🇼 Curazao | 1 | -7.41 |

### Grupo F

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-14 | 🇳🇱 Países Bajos – 🇯🇵 Japón | **2-2** | 0% | 100% | 0% |
| 06-15 | 🇸🇪 Suecia – 🇹🇳 Túnez | **5-1** | 100% | 0% | 0% |
| 06-20 | 🇳🇱 Países Bajos – 🇸🇪 Suecia | **5-1** | 100% | 0% | 0% |
| 06-21 | 🇹🇳 Túnez – 🇯🇵 Japón | **0-4** | 0% | 0% | 100% |
| 06-26 | 🇹🇳 Túnez – 🇳🇱 Países Bajos | **0-1** | 17% | 27% | 56% |
| 06-26 | 🇯🇵 Japón – 🇸🇪 Suecia | **2-1** | 56% | 27% | 17% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇳🇱 Países Bajos ✅ | 7 | +4.60 |
| 2 | 🇯🇵 Japón ✅ | 7 | +4.15 |
| 3 | 🇸🇪 Suecia 🟡 | 3 | -0.15 |
| 4 | 🇹🇳 Túnez | 0 | -8.60 |

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
| 1 | 🇧🇪 Bélgica ✅ | 5 | +1.67 |
| 2 | 🇮🇷 Irán ✅ | 5 | +0.28 |
| 3 | 🇪🇬 Egipto 🟡 | 4 | +1.72 |
| 4 | 🇳🇿 Nueva Zelanda | 1 | -3.67 |

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
| 1 | 🇪🇸 España ✅ | 7 | +4.94 |
| 2 | 🇸🇦 Arabia Saudí ✅ | 4 | -4.32 |
| 3 | 🇨🇻 Cabo Verde 🟡 | 2 | +0.32 |
| 4 | 🇺🇾 Uruguay | 2 | -0.94 |

### Grupo I

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-16 | 🇫🇷 Francia – 🇸🇳 Senegal | **3-1** | 100% | 0% | 0% |
| 06-17 | 🇮🇶 Irak – 🇳🇴 Noruega | **1-4** | 0% | 0% | 100% |
| 06-22 | 🇫🇷 Francia – 🇮🇶 Irak | **3-0** | 100% | 0% | 0% |
| 06-23 | 🇳🇴 Noruega – 🇸🇳 Senegal | **3-2** | 100% | 0% | 0% |
| 06-26 | 🇳🇴 Noruega – 🇫🇷 Francia | **0-2** | 9% | 25% | 66% |
| 06-26 | 🇸🇳 Senegal – 🇮🇶 Irak | **2-0** | 67% | 22% | 10% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇫🇷 Francia ✅ | 9 | +6.16 |
| 2 | 🇳🇴 Noruega ✅ | 6 | +2.84 |
| 3 | 🇸🇳 Senegal 🟡 | 3 | -1.62 |
| 4 | 🇮🇶 Irak | 0 | -7.38 |

### Grupo J

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-17 | 🇦🇷 Argentina – 🇩🇿 Argelia | **3-0** | 100% | 0% | 0% |
| 06-17 | 🇦🇹 Austria – 🇯🇴 Jordania | **3-1** | 100% | 0% | 0% |
| 06-22 | 🇦🇷 Argentina – 🇦🇹 Austria | **2-0** | 100% | 0% | 0% |
| 06-23 | 🇯🇴 Jordania – 🇩🇿 Argelia | **2-1** | 100% | 0% | 0% |
| 06-28 | 🇩🇿 Argelia – 🇦🇹 Austria | **0-1** | 30% | 29% | 41% |
| 06-28 | 🇯🇴 Jordania – 🇦🇷 Argentina | **0-3** | 6% | 16% | 78% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇦🇷 Argentina ✅ | 9 | +7.28 |
| 2 | 🇦🇹 Austria ✅ | 6 | +0.26 |
| 3 | 🇯🇴 Jordania 🟡 | 3 | -3.28 |
| 4 | 🇩🇿 Argelia | 0 | -4.26 |

### Grupo K

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-17 | 🇵🇹 Portugal – 🇨🇩 RD Congo | **1-1** | 0% | 100% | 0% |
| 06-18 | 🇺🇿 Uzbekistán – 🇨🇴 Colombia | **1-3** | 0% | 0% | 100% |
| 06-23 | 🇵🇹 Portugal – 🇺🇿 Uzbekistán | **3-0** | 62% | 26% | 11% |
| 06-24 | 🇨🇴 Colombia – 🇨🇩 RD Congo | **1-0** | 50% | 31% | 20% |
| 06-28 | 🇨🇩 RD Congo – 🇺🇿 Uzbekistán | **1-0** | 46% | 32% | 22% |
| 06-28 | 🇨🇴 Colombia – 🇵🇹 Portugal | **1-2** | 21% | 35% | 45% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🇵🇹 Portugal ✅ | 7 | +3.05 |
| 2 | 🇨🇴 Colombia ✅ | 6 | +1.62 |
| 3 | 🇨🇩 RD Congo 🟡 | 4 | -0.10 |
| 4 | 🇺🇿 Uzbekistán | 0 | -4.57 |

### Grupo L

| Fecha | Partido | Pred. | P(1) | P(X) | P(2) |
|---|---|:-:|--:|--:|--:|
| 06-17 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra – 🇭🇷 Croacia | **4-2** | 100% | 0% | 0% |
| 06-18 | 🇬🇭 Ghana – 🇵🇦 Panamá | **1-0** | 100% | 0% | 0% |
| 06-23 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra – 🇬🇭 Ghana | **2-0** | 74% | 18% | 8% |
| 06-24 | 🇵🇦 Panamá – 🇭🇷 Croacia | **0-2** | 15% | 24% | 61% |
| 06-27 | 🇭🇷 Croacia – 🇬🇭 Ghana | **2-0** | 71% | 21% | 8% |
| 06-27 | 🇵🇦 Panamá – 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | **0-3** | 12% | 28% | 60% |

| Pos | Equipo | Pts | DG (xG) |
|---|---|--:|--:|
| 1 | 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra ✅ | 9 | +5.21 |
| 2 | 🇭🇷 Croacia ✅ | 6 | +0.61 |
| 3 | 🇬🇭 Ghana 🟡 | 3 | -1.59 |
| 4 | 🇵🇦 Panamá | 0 | -4.23 |

✅ clasificado directo · 🟡 tercero (pasan los 8 mejores)

## Eliminatorias — 32 partidos

Si el empate es el resultado más probable, el cruce se decide por penaltis a favor del equipo con mayor probabilidad de victoria.

### Dieciseisavos de final (16 cruces) · *28 jun - 3 jul*

| Cruce | Pred. | Avanza | P(1) | P(X) | P(2) |
|---|:-:|---|--:|--:|--:|
| 🇩🇪 Alemania – 🇪🇬 Egipto | **2-0** | **🇩🇪 Alemania** | 58% | 31% | 11% |
| 🇫🇷 Francia – 🇨🇩 RD Congo | **2-0** | **🇫🇷 Francia** | 70% | 22% | 8% |
| 🇰🇷 Corea del Sur – 🇨🇦 Canadá | **1-0** | **🇰🇷 Corea del Sur** | 41% | 32% | 27% |
| 🇳🇱 Países Bajos – 🇲🇦 Marruecos | **1-0** | **🇳🇱 Países Bajos** | 54% | 26% | 19% |
| 🇨🇴 Colombia – 🇭🇷 Croacia | **1-2** | **🇭🇷 Croacia** | 15% | 32% | 53% |
| 🇪🇸 España – 🇦🇹 Austria | **2-1** | **🇪🇸 España** | 48% | 31% | 20% |
| 🇺🇸 EE. UU. – 🇶🇦 Catar | **2-0** | **🇺🇸 EE. UU.** | 48% | 35% | 17% |
| 🇧🇪 Bélgica – 🇸🇪 Suecia | **2-1** | **🇧🇪 Bélgica** | 59% | 26% | 14% |
| 🇧🇷 Brasil – 🇯🇵 Japón | **1-1 (pen)** | **🇧🇷 Brasil** | 34% | 43% | 23% |
| 🇨🇮 Costa de Marfil – 🇳🇴 Noruega | **1-0** | **🇨🇮 Costa de Marfil** | 53% | 28% | 19% |
| 🇲🇽 México – 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia | **2-1** | **🇲🇽 México** | 54% | 34% | 12% |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra – 🇬🇭 Ghana | **2-0** | **🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra** | 74% | 18% | 8% |
| 🇦🇷 Argentina – 🇸🇦 Arabia Saudí | **3-0** | **🇦🇷 Argentina** | 76% | 17% | 7% |
| 🇦🇺 Australia – 🇮🇷 Irán | **0-1** | **🇮🇷 Irán** | 16% | 30% | 55% |
| 🇨🇭 Suiza – 🇸🇳 Senegal | **1-2** | **🇸🇳 Senegal** | 21% | 33% | 46% |
| 🇵🇹 Portugal – 🇵🇾 Paraguay | **2-0** | **🇵🇹 Portugal** | 59% | 26% | 15% |

### Octavos de final · *4 - 7 jul*

| Cruce | Pred. | Avanza | P(1) | P(X) | P(2) |
|---|:-:|---|--:|--:|--:|
| 🇩🇪 Alemania – 🇫🇷 Francia | **1-1 (pen)** | **🇫🇷 Francia** | 25% | 47% | 28% |
| 🇰🇷 Corea del Sur – 🇳🇱 Países Bajos | **0-1** | **🇳🇱 Países Bajos** | 24% | 37% | 38% |
| 🇭🇷 Croacia – 🇪🇸 España | **1-2** | **🇪🇸 España** | 21% | 38% | 41% |
| 🇺🇸 EE. UU. – 🇧🇪 Bélgica | **0-1** | **🇧🇪 Bélgica** | 21% | 37% | 43% |
| 🇧🇷 Brasil – 🇨🇮 Costa de Marfil | **1-1 (pen)** | **🇧🇷 Brasil** | 31% | 42% | 28% |
| 🇲🇽 México – 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | **1-1 (pen)** | **🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra** | 29% | 38% | 32% |
| 🇦🇷 Argentina – 🇮🇷 Irán | **1-0** | **🇦🇷 Argentina** | 42% | 40% | 18% |
| 🇸🇳 Senegal – 🇵🇹 Portugal | **0-1** | **🇵🇹 Portugal** | 28% | 35% | 37% |

### Cuartos de final · *9 - 11 jul*

| Cruce | Pred. | Avanza | P(1) | P(X) | P(2) |
|---|:-:|---|--:|--:|--:|
| 🇫🇷 Francia – 🇳🇱 Países Bajos | **2-1** | **🇫🇷 Francia** | 52% | 32% | 16% |
| 🇪🇸 España – 🇧🇪 Bélgica | **2-1** | **🇪🇸 España** | 36% | 35% | 29% |
| 🇧🇷 Brasil – 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | **1-2** | **🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra** | 24% | 37% | 39% |
| 🇦🇷 Argentina – 🇵🇹 Portugal | **1-1 (pen)** | **🇦🇷 Argentina** | 36% | 44% | 20% |

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
| 🇫🇷 Francia | 100.0% | 84.1% | 50.7% | 40.5% | 25.9% | **17.2%** |
| 🇦🇷 Argentina | 100.0% | 84.3% | 60.1% | 43.2% | 26.6% | **14.5%** |
| 🇪🇸 España | 100.0% | 68.9% | 49.5% | 36.0% | 21.9% | **13.1%** |
| 🇩🇪 Alemania | 100.0% | 75.2% | 40.0% | 29.7% | 16.9% | **9.4%** |
| 🏴󠁧󠁢󠁥󠁮󠁧󠁿 Inglaterra | 99.7% | 77.6% | 45.4% | 31.4% | 17.7% | **9.3%** |
| 🇧🇪 Bélgica | 90.7% | 73.6% | 42.9% | 24.8% | 11.9% | **5.3%** |
| 🇭🇷 Croacia | 88.5% | 57.8% | 31.6% | 21.1% | 10.3% | **5.1%** |
| 🇵🇹 Portugal | 91.1% | 63.5% | 37.5% | 18.6% | 9.7% | **4.8%** |
| 🇧🇷 Brasil | 100.0% | 62.1% | 37.3% | 18.1% | 9.0% | **4.1%** |
| 🇲🇽 México | 100.0% | 72.6% | 37.5% | 19.5% | 9.0% | **3.4%** |
| 🇨🇮 Costa de Marfil | 98.5% | 67.6% | 36.0% | 15.1% | 6.5% | **2.8%** |
| 🇸🇳 Senegal | 49.6% | 31.4% | 22.0% | 11.3% | 5.7% | **2.4%** |
| 🇳🇱 Países Bajos | 100.0% | 58.6% | 34.4% | 10.5% | 4.4% | **1.8%** |
| 🇯🇵 Japón | 100.0% | 43.5% | 22.0% | 7.4% | 2.9% | **1.2%** |
| 🇮🇷 Irán | 86.8% | 55.2% | 23.1% | 8.4% | 3.1% | **1.0%** |
| 🇨🇴 Colombia | 98.7% | 51.0% | 24.6% | 9.0% | 3.2% | **1.0%** |
| 🇨🇭 Suiza | 100.0% | 58.7% | 25.7% | 6.7% | 2.5% | **0.7%** |
| 🇺🇸 EE. UU. | 100.0% | 66.8% | 34.6% | 9.4% | 2.4% | **0.7%** |
| 🇺🇾 Uruguay | 49.0% | 25.0% | 11.1% | 4.9% | 1.8% | **0.4%** |
| 🇦🇹 Austria | 100.0% | 33.0% | 11.8% | 5.2% | 1.6% | **0.4%** |
| 🇲🇦 Marruecos | 100.0% | 36.3% | 18.3% | 5.3% | 1.6% | **0.4%** |
| 🇰🇷 Corea del Sur | 97.3% | 45.4% | 18.7% | 3.9% | 1.2% | **0.3%** |
| 🇳🇴 Noruega | 100.0% | 34.7% | 11.5% | 3.4% | 1.0% | **0.2%** |
| 🇨🇦 Canadá | 100.0% | 49.5% | 17.9% | 4.2% | 1.0% | **0.2%** |
| 🇸🇪 Suecia | 99.3% | 27.7% | 8.6% | 2.2% | 0.6% | **0.1%** |
| 🇪🇬 Egipto | 100.0% | 38.6% | 10.9% | 2.5% | 0.4% | **0.1%** |
| 🇦🇺 Australia | 99.9% | 23.7% | 4.4% | 1.2% | 0.2% | **0.0%** |
| 🏴󠁧󠁢󠁳󠁣󠁴󠁿 Escocia | 98.1% | 23.2% | 5.9% | 1.1% | 0.2% | **0.0%** |
| 🇨🇻 Cabo Verde | 68.8% | 10.0% | 2.6% | 0.7% | 0.1% | **0.0%** |
| 🇬🇭 Ghana | 91.1% | 20.7% | 4.6% | 0.8% | 0.1% | **0.0%** |
| 🇿🇦 Sudáfrica | 21.8% | 9.7% | 3.5% | 0.7% | 0.2% | **0.0%** |
| 🇨🇩 RD Congo | 68.3% | 17.2% | 3.7% | 0.9% | 0.1% | **0.0%** |
| 🇧🇦 Bosnia-Herzegovina | 28.2% | 5.5% | 1.4% | 0.3% | 0.1% | **0.0%** |
| 🇪🇨 Ecuador | 13.8% | 4.2% | 1.7% | 0.4% | 0.1% | **0.0%** |
| 🇵🇾 Paraguay | 79.4% | 12.7% | 2.6% | 0.4% | 0.0% | **0.0%** |
| 🇶🇦 Catar | 38.3% | 9.2% | 2.5% | 0.4% | 0.0% | **0.0%** |
| 🇵🇦 Panamá | 9.2% | 2.1% | 0.3% | 0.1% | 0.0% | **0.0%** |
| 🇺🇿 Uzbekistán | 15.5% | 3.6% | 0.6% | 0.1% | 0.0% | **0.0%** |
| 🇯🇴 Jordania | 52.0% | 5.2% | 0.9% | 0.1% | 0.0% | **0.0%** |
| 🇸🇦 Arabia Saudí | 33.4% | 3.0% | 0.4% | 0.1% | 0.0% | **0.0%** |
| 🇨🇿 República Checa | 10.4% | 2.1% | 0.3% | 0.1% | 0.0% | **0.0%** |
| 🇳🇿 Nueva Zelanda | 9.6% | 3.1% | 0.4% | 0.0% | 0.0% | **0.0%** |
| 🇮🇶 Irak | 2.6% | 0.4% | 0.1% | 0.0% | 0.0% | **0.0%** |
| 🇩🇿 Argelia | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| 🇨🇼 Curazao | 10.4% | 1.5% | 0.2% | 0.0% | 0.0% | **0.0%** |
| 🇭🇹 Haití | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| 🇹🇷 Turquía | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |
| 🇹🇳 Túnez | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | **0.0%** |

## Validación con los partidos ya jugados

| Partido | Predicción del modelo | Resultado real |
|---|:-:|:-:|
| 🇲🇽 México – 🇿🇦 Sudáfrica | 2-0 (P1 100%) | 2-0 ✅ ganador acertado |
| 🇰🇷 Corea del Sur – 🇨🇿 República Checa | 2-1 (P1 100%) | 2-1 ✅ ganador acertado |

---
*Predicciones generadas automáticamente con `prediccion_mundial.py`. El fútbol, por suerte, no entiende de modelos.* ⚽