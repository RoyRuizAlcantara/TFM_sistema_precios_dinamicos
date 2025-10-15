import pandas as pd
import json
import random
from datetime import datetime, timedelta
import os
from src.utils import clean_and_parse_price


NUM_STORES = 10
NUM_SALES_RECORDS = 5000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2024, 10, 1)


def generate_data_from_scrape(project_root):
    """
    Genera TODOS los datos sintéticos (internos y externos) usando la ruta del proyecto.
    """
    # Definición de Rutas
    SCRAPED_DATA_PATH = os.path.join(project_root, 'data', 'scraped_data', 'suburbia_products.json')
    INTERNAL_DATA_PATH = os.path.join(project_root, 'data', 'synthetic_data', 'internal')
    EXTERNAL_DATA_PATH = os.path.join(project_root, 'data', 'synthetic_data', 'external')

    # Creación de Directorios
    os.makedirs(INTERNAL_DATA_PATH, exist_ok=True)
    os.makedirs(EXTERNAL_DATA_PATH, exist_ok=True)

    print(f"--- Generador: Leyendo de '{SCRAPED_DATA_PATH}' y guardando en carpetas internal/ y external/")
    print("--- Iniciando Generación de Datos Sintéticos v2 (Basado en Scraping) ---")

    # =============================================================
    # SECCIÓN 1: GENERACIÓN DE DATOS INTERNOS
    # =============================================================
    try:
        df_competitor = pd.read_json(SCRAPED_DATA_PATH)
        print(f"Cargados {len(df_competitor)} productos de '{SCRAPED_DATA_PATH}'")

        # Si el scraper falla y el archivo está vacío, detenemos esta parte.
        if df_competitor.empty:
            raise ValueError("El archivo de scraping está vacío.")

    except (FileNotFoundError, ValueError) as e:
        print(f"ADVERTENCIA: No se pudieron generar datos internos. Causa: {e}")
        print("El pipeline continuará sin datos internos actualizados.")
        return  # Detenemos la función si no hay datos de entrada.

    df_competitor['base_price'] = df_competitor['precio_descuento'].apply(clean_and_parse_price)
    df_competitor.dropna(subset=['base_price'], inplace=True)

    # a. Catálogo de Productos
    print("\nGenerando catálogo de productos interno...")
    product_catalog = []
    for idx, row in df_competitor.iterrows():
        product_catalog.append({
            'sku': f'SKU{1000 + idx}',
            'product_name': row['nombre_producto'],
            'category': 'Zapatos Deportivos',
            'base_price': row['base_price'],
            'competitor_sku': row['sku_competidor']
        })
    df_catalog = pd.DataFrame(product_catalog)
    df_catalog.to_csv(os.path.join(INTERNAL_DATA_PATH, 'product_catalog.csv'), index=False)
    print(f"Catálogo interno guardado. Contiene {len(df_catalog)} productos.")

    # b. Inventario
    print("\nGenerando datos de inventario...")
    inventory = []
    for i in range(NUM_STORES):
        store_id = 100 + i
        for sku in df_catalog['sku']:
            inventory.append({
                'id_tienda': store_id,
                'sku': sku,
                'stock_disponible': random.randint(5, 100)
            })
    df_inventory = pd.DataFrame(inventory)
    df_inventory.to_csv(os.path.join(INTERNAL_DATA_PATH, 'inventory.csv'), index=False)
    print(f"Inventario guardado para {NUM_STORES} tiendas.")

    # c. Ventas (POS)
    print("\nGenerando datos de ventas...")
    sales = []
    for _ in range(NUM_SALES_RECORDS):
        store_id = random.randint(100, 100 + NUM_STORES - 1)
        sku_info = df_catalog.sample(1).iloc[0]

        total_days = (END_DATE - START_DATE).days
        random_days = random.randint(0, total_days)
        date = START_DATE + timedelta(days=random_days)

        quantity = random.randint(1, 3)
        price_modifier = random.uniform(0.9, 1.1)
        final_price = round(sku_info['base_price'] * price_modifier * quantity, 2)

        sales.append({
            'id_tienda': store_id,
            'sku': sku_info['sku'],
            'fecha': date.strftime('%Y-%m-%d'),
            'cantidad_vendida': quantity,
            'precio_final': final_price
        })
    df_sales = pd.DataFrame(sales)
    df_sales.to_csv(os.path.join(INTERNAL_DATA_PATH, 'daily_sales.csv'), index=False)
    print(f"Datos de ventas guardados ({NUM_SALES_RECORDS} registros).")

    # =============================================================
    # SECCIÓN 2: GENERACIÓN DE DATOS EXTERNOS
    # =============================================================
    print("\nGenerando datos externos (Clima y Demografía)...")
    states_mx = ['Ciudad de México', 'Jalisco', 'Nuevo León', 'Puebla', 'Estado de México', 'Veracruz']

    # a. Datos Climáticos (simulando una respuesta de API)
    weather_data = []
    for state in states_mx:
        weather_data.append({
            'estado': state,
            'fecha_consulta': datetime.now().date().isoformat(),
            'temp_max': round(random.uniform(20.0, 35.0), 1),
            'temp_min': round(random.uniform(8.0, 19.0), 1),
            'condicion': random.choice(['Soleado', 'Nublado', 'Lluvioso'])
        })
    with open(os.path.join(EXTERNAL_DATA_PATH, 'weather_data.json'), 'w', encoding='utf-8') as f:
        json.dump(weather_data, f, indent=4, ensure_ascii=False)
    print("Datos climáticos guardados.")

    # b. Datos Demográficos (simulando respuesta de API de INEGI)
    demographic_data = []
    for state in states_mx:
        demographic_data.append({
            'estado': state,
            'poblacion_total': random.randint(1_000_000, 15_000_000),
            'ingreso_promedio_mensual': round(random.uniform(8000, 25000), 2),
            'fuente': 'INEGI (Simulado)'
        })
    with open(os.path.join(EXTERNAL_DATA_PATH, 'demographic_data.json'), 'w', encoding='utf-8') as f:
        json.dump(demographic_data, f, indent=4, ensure_ascii=False)
    print("Datos demográficos guardados.")

    print("\n--- Proceso completo de generación de datos sintéticos finalizado. ---")


if __name__ == "__main__":
    project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    generate_data_from_scrape(project_root_path)