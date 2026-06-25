# -*- coding: utf-8 -*-
"""Scraper incremental de partidos recientes de Flashscore.

Uso:
    python 01_Scraping/scrapear_incremental.py --urls Data/urls_incremental_junio.txt

Requiere Chrome abierto en modo depuracion remota:
    chrome.exe --remote-debugging-port=9222

El script no reemplaza `Data/partidos.csv`: agrega las URLs nuevas y deduplica
por URL, fecha y equipos. Despues conviene correr:

    python 02_Limpieza_Datos/Data_Cleaning.py --features-hasta 2026-06-25
"""

import argparse
import os
import random
import time

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from Scrapper import extraer_partido_completo, aplanar_datos


RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUTA_PARTIDOS = os.path.join(RAIZ, 'Data', 'partidos.csv')


def leer_urls(ruta):
    with open(ruta, encoding='utf-8') as f:
        return [
            linea.strip()
            for linea in f
            if linea.strip() and not linea.lstrip().startswith('#')
        ]


def conectar_chrome():
    opciones = Options()
    opciones.add_experimental_option('debuggerAddress', '127.0.0.1:9222')
    servicio = Service(ChromeDriverManager().install())
    return webdriver.Chrome(service=servicio, options=opciones)


def main():
    parser = argparse.ArgumentParser(description='Agrega partidos recientes a Data/partidos.csv')
    parser.add_argument('--urls', required=True, help='Archivo TXT con URLs de Flashscore, una por linea.')
    parser.add_argument('--salida', default=RUTA_PARTIDOS, help='CSV de partidos a actualizar.')
    parser.add_argument('--pausa-min', type=float, default=2.0)
    parser.add_argument('--pausa-max', type=float, default=4.5)
    args = parser.parse_args()

    urls = leer_urls(args.urls)
    if not urls:
        raise SystemExit(f'No hay URLs para procesar en {args.urls}')

    df_existente = (
        pd.read_csv(args.salida)
        if os.path.exists(args.salida)
        else pd.DataFrame()
    )
    urls_existentes = set(df_existente.get('URL', pd.Series(dtype=str)).dropna().astype(str))
    urls_nuevas = [u for u in urls if u not in urls_existentes]
    print(f'URLs recibidas: {len(urls)} | nuevas: {len(urls_nuevas)}')

    if not urls_nuevas:
        print('No hay URLs nuevas. Nada que agregar.')
        return

    driver = conectar_chrome()
    filas = []
    try:
        for i, url in enumerate(urls_nuevas, 1):
            print(f'[{i}/{len(urls_nuevas)}] {url}')
            datos = extraer_partido_completo(url, driver)
            if datos and datos.get('equipo_local') != 'Desconocido':
                filas.append(aplanar_datos(datos))
            else:
                print(f'  No se pudo extraer: {url}')
            if i < len(urls_nuevas):
                time.sleep(random.uniform(args.pausa_min, args.pausa_max))
    finally:
        driver.quit()

    if not filas:
        print('No se extrajo ningun partido nuevo.')
        return

    df_nuevo = pd.DataFrame(filas)
    df_final = pd.concat([df_existente, df_nuevo], ignore_index=True, sort=False)
    df_final.drop_duplicates(
        subset=['URL', 'Fecha', 'Equipo_Local', 'Equipo_Visitante'],
        keep='last',
        inplace=True,
    )
    os.makedirs(os.path.dirname(args.salida), exist_ok=True)
    df_final.to_csv(args.salida, index=False, encoding='utf-8-sig')
    print(f'Partidos agregados: {len(df_nuevo)} | total en {args.salida}: {len(df_final)}')


if __name__ == '__main__':
    main()
