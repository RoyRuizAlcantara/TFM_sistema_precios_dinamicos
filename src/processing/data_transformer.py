import pandas as pd
import os
import json
from src.utils import clean_and_parse_price


def transform_data(project_root):
    """
    Carga, limpia, integra y transforma los datos de diversas fuentes
    en una única tabla analítica, usando la ruta del proyecto proporcionada.
    """
    INTERNAL_PATH = os.path.join(project_root, 'data', 'synthetic_data', 'internal')
    SCRAPED_PATH = os.path.join(project_root, 'data', 'scraped_data')
    PROCESSED_PATH = os.path.join(project_root, 'data', 'processed')
    os.makedirs(PROCESSED_PATH, exist_ok=True)
    print(f"--- Transformador: Guardando datos en: {PROCESSED_PATH}")

    print("--- Iniciando Fase 3: Transformación de Datos ---")

    print("Cargando archivos de datos...")
    try:
        df_sales = pd.read_csv(os.path.join(INTERNAL_PATH, 'daily_sales.csv'))
        df_inventory = pd.read_csv(os.path.join(INTERNAL_PATH, 'inventory.csv'))
        df_catalog = pd.read_csv(os.path.join(INTERNAL_PATH, 'product_catalog.csv'))

        df_competitor_raw = pd.read_json(os.path.join(SCRAPED_PATH, 'suburbia_products.json'))
        df_competitor_raw['competitor_price'] = df_competitor_raw['precio_descuento'].apply(clean_and_parse_price)
        df_competitor = df_competitor_raw[['sku_competidor', 'competitor_price']].copy()

    except FileNotFoundError as e:
        print(f"Error: Archivo no encontrado. Asegúrate de haber generado los datos. ({e})")
        return
    except ValueError as e:
        print(f"Error: Uno de los archivos de entrada está vacío o mal formateado. ({e})")
        return

    print("Limpiando y pre-procesando datos...")
    df_sales['fecha'] = pd.to_datetime(df_sales['fecha'])
    df_sales['precio_unitario'] = df_sales['precio_final'] / df_sales['cantidad_vendida']

    print("Integrando fuentes de datos...")
    df_merged = pd.merge(df_sales, df_catalog, on='sku', how='left')
    df_merged = pd.merge(df_merged, df_inventory, on=['sku', 'id_tienda'], how='left')
    df_merged = pd.merge(df_merged, df_competitor,
                         left_on='competitor_sku', right_on='sku_competidor',
                         how='left')

    df_final = df_merged[[
        'fecha', 'id_tienda', 'sku', 'product_name', 'base_price',
        'precio_unitario', 'cantidad_vendida', 'stock_disponible', 'competitor_price'
    ]].copy()
    df_final.rename(columns={'base_price': 'precio_base_interno'}, inplace=True)

    output_file = os.path.join(PROCESSED_PATH, 'analytical_base_table.csv')
    df_final.to_csv(output_file, index=False)

    print("\n--- Transformación Completada ---")
    print(f"Tabla analítica guardada en: '{output_file}'")
    print("Primeras 5 filas de la tabla final:")
    print(df_final.head())


if __name__ == "__main__":
    project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    transform_data(project_root_path)