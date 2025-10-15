import pandas as pd
import os
import numpy as np


def recommend_prices(project_root):
    """
    Carga la tabla analítica y aplica reglas de negocio para
    generar un nuevo set de precios recomendados, usando la ruta del proyecto.
    """
    PROCESSED_PATH = os.path.join(project_root, 'data', 'processed')
    RECOMMENDATIONS_PATH = os.path.join(project_root, 'data', 'recommendations')
    os.makedirs(RECOMMENDATIONS_PATH, exist_ok=True)
    print(f"--- Modelo: Guardando recomendaciones en: {RECOMMENDATIONS_PATH}")

    print("--- Iniciando Fase 4: Modelo de Recomendación de Precios (Basado en Reglas) ---")

    abt_path = os.path.join(PROCESSED_PATH, 'analytical_base_table.csv')
    try:
        df = pd.read_csv(abt_path)
        df['fecha'] = pd.to_datetime(df['fecha'])
        df_current_state = df.sort_values('fecha').groupby(['sku', 'id_tienda']).last().reset_index()
        print(f"Cargada la tabla analítica con {len(df_current_state)} registros de estado actual.")
    except FileNotFoundError:
        print(f"Error: No se encontró la tabla analítica en '{abt_path}'. Ejecuta el script de transformación primero.")
        return

    print("Aplicando reglas de negocio para generar recomendaciones...")

    recommendations = []

    for _, row in df_current_state.iterrows():
        current_price = row['precio_unitario']
        competitor_price = row['competitor_price']
        stock = row['stock_disponible']
        base_price = row['precio_base_interno']

        recommended_price = current_price
        reason = "Mantener Precio Actual"

        if pd.notna(competitor_price) and current_price > (competitor_price * 1.05):
            recommended_price = competitor_price
            reason = "Ajuste por Competencia"

        if stock > 50:
            recommended_price = base_price * 0.95
            reason = "Descuento por Alto Inventario"

        if stock < 10:
            recommended_price = base_price * 1.10
            reason = "Aumento por Bajo Inventario"

        recommendations.append({
            'sku': row['sku'],
            'id_tienda': row['id_tienda'],
            'product_name': row['product_name'],
            'precio_actual': round(current_price, 2),
            'stock_actual': int(stock),
            'precio_competidor': round(competitor_price, 2) if pd.notna(competitor_price) else None,
            'precio_recomendado': round(recommended_price, 2),
            'justificacion': reason
        })

    df_recommendations = pd.DataFrame(recommendations)

    output_file = os.path.join(RECOMMENDATIONS_PATH, 'recommended_prices.csv')
    df_recommendations.to_csv(output_file, index=False)

    print("\n--- Modelo de Recomendación Completado ---")
    print(f"Recomendaciones de precios guardadas en: '{output_file}'")
    print("Primeras 5 recomendaciones:")
    print(df_recommendations.head())


if __name__ == "__main__":
    project_root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    recommend_prices(project_root_path)