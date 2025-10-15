import pandas as pd
from faker import Faker
import random
from datetime import datetime, timedelta
import os

# Inicializar Faker para datos en español de México
fake = Faker('es_MX')

# --- CONFIGURACIÓN ---
NUM_STORES = 10
NUM_SKUS = 50  # Zapatos deportivos
NUM_SALES_RECORDS = 5000
START_DATE = datetime(2023, 1, 1)
END_DATE = datetime(2023, 12, 31)

# --- RUTAS DE SALIDA ---
INTERNAL_DATA_PATH = '../../../data/synthetic_data/internal/'
EXTERNAL_DATA_PATH = '../../../data/synthetic_data/external/'

# Asegurarse de que los directorios existan
os.makedirs(INTERNAL_DATA_PATH, exist_ok=True)
os.makedirs(EXTERNAL_DATA_PATH, exist_ok=True)


# --- 1. GENERACIÓN DE DATOS INTERNOS ---

# a. Catálogo de Productos
print("Generando catálogo de productos...")
product_catalog = []
for i in range(NUM_SKUS):
    product_name = f"Tenis deportivos {fake.company_suffix()} {random.choice(['Runner', 'Fly', 'Max', 'Pro'])} {i+1}"
    product_catalog.append({
        'sku': f'SKU{1000 + i}',
        'product_name': product_name,
        'category': 'Zapatos Deportivos',
        'base_price': round(random.uniform(899.99, 2999.99), 2)
    })
df_catalog = pd.DataFrame(product_catalog)
df_catalog.to_csv(os.path.join(INTERNAL_DATA_PATH, 'product_catalog.csv'), index=False)
print(f"Catálogo guardado en: {os.path.join(INTERNAL_DATA_PATH, 'product_catalog.csv')}")


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
print(f"Inventario guardado en: {os.path.join(INTERNAL_DATA_PATH, 'inventory.csv')}")


# c. Ventas (POS)
print("\nGenerando datos de ventas...")
sales = []
for _ in range(NUM_SALES_RECORDS):
    store_id = random.randint(100, 100 + NUM_STORES - 1)
    sku_info = df_catalog.sample(1).iloc[0]
    date = fake.date_between(start_date=START_DATE, end_date=END_DATE)
    quantity = random.randint(1, 5)
    # Simular un descuento aleatorio
    discount = random.choice([0, 0.1, 0.15, 0.2])
    final_price = round(sku_info['base_price'] * (1 - discount) * quantity, 2)

    sales.append({
        'id_tienda': store_id,
        'sku': sku_info['sku'],
        'fecha': date,
        'cantidad_vendida': quantity,
        'precio_final': final_price
    })
df_sales = pd.DataFrame(sales)
df_sales.to_csv(os.path.join(INTERNAL_DATA_PATH, 'daily_sales.csv'), index=False)
print(f"Ventas guardadas en: {os.path.join(INTERNAL_DATA_PATH, 'daily_sales.csv')}")


# --- 2. GENERACIÓN DE DATOS EXTERNOS (SIMULADOS) ---

# a. Precios de la Competencia (simulando un JSON de scraping)
print("\nGenerando datos de competencia...")
competitor_prices = []
for sku_info in df_catalog.sample(15).to_dict('records'): # Simular 15 productos de la competencia
    competitor_prices.append({
        'sku_competidor': sku_info['sku'],
        'nombre_producto': sku_info['product_name'],
        'precio_lista': round(sku_info['base_price'] * random.uniform(0.98, 1.1), 2),
        'precio_descuento': round(sku_info['base_price'] * random.uniform(0.8, 1.0), 2),
        'url_producto': f"http://competidor.com/producto/{sku_info['sku']}",
        'fecha_extraccion': datetime.now().isoformat()
    })
df_competitor = pd.DataFrame(competitor_prices)
df_competitor.to_json(os.path.join(EXTERNAL_DATA_PATH, 'competitor_prices.json'), orient='records', indent=4)
print(f"Datos de competencia guardados en: {os.path.join(EXTERNAL_DATA_PATH, 'competitor_prices.json')}")


# b. Datos Climáticos (simulando una respuesta de API)
print("\nGenerando datos climáticos...")
weather_data = []
states_mx = ['Ciudad de México', 'Jalisco', 'Nuevo León', 'Puebla', 'Estado de México']
for state in states_mx:
    weather_data.append({
        'estado': state,
        'fecha_consulta': datetime.now().date().isoformat(),
        'temp_max': round(random.uniform(20.0, 35.0), 1),
        'temp_min': round(random.uniform(8.0, 19.0), 1),
        'condicion': random.choice(['Soleado', 'Nublado', 'Lluvioso'])
    })
df_weather = pd.DataFrame(weather_data)
df_weather.to_json(os.path.join(EXTERNAL_DATA_PATH, 'weather_data.json'), orient='records', indent=4)
print(f"Datos climáticos guardados en: {os.path.join(EXTERNAL_DATA_PATH, 'weather_data.json')}")


# c. Datos Demográficos (simulando respuesta de API de INEGI)
print("\nGenerando datos demográficos...")
demographic_data = []
for state in states_mx:
    demographic_data.append({
        'estado': state,
        'poblacion_total': random.randint(1_000_000, 15_000_000),
        'ingreso_promedio_mensual': round(random.uniform(8000, 25000), 2),
        'fuente': 'INEGI (Simulado)'
    })
df_demographic = pd.DataFrame(demographic_data)
df_demographic.to_json(os.path.join(EXTERNAL_DATA_PATH, 'demographic_data.json'), orient='records', indent=4)
print(f"Datos demográficos guardados en: {os.path.join(EXTERNAL_DATA_PATH, 'demographic_data.json')}")

print("\n--- Proceso de generación de datos sintéticos completado. ---")