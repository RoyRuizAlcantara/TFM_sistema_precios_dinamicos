import os
from src.ingestion.web_scraping.suburbia_scraper import scrape_suburbia_selenium
from src.ingestion.data_generation.synthetic_data_generator_v2 import generate_data_from_scrape
from src.processing.data_transformer import transform_data
from src.modeling.pricing_model import recommend_prices


def run_pipeline():
    """
    Ejecuta el pipeline de datos completo, definiendo y pasando la ruta raíz del proyecto.
    """
    PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    print("==============================================")
    print(f"== INICIANDO PIPELINE (RAÍZ: {PROJECT_ROOT}) ==")
    print("==============================================")

    print("\n[PASO 1/4] Ejecutando Web Scraper...")
    scrape_suburbia_selenium(PROJECT_ROOT)

    print("\n[PASO 2/4] Ejecutando Generador de Datos Sintéticos...")
    generate_data_from_scrape(PROJECT_ROOT)

    print("\n[PASO 3/4] Ejecutando Transformación de Datos...")
    transform_data(PROJECT_ROOT)

    print("\n[PASO 4/4] Ejecutando Modelo de Recomendación...")
    recommend_prices(PROJECT_ROOT)

    print("\n=============================================")
    print("== PIPELINE COMPLETADO CON ÉXITO ==")
    print("=============================================")


if __name__ == "__main__":
    run_pipeline()