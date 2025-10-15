import time
import json
import os
import re
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
from src.utils import clean_and_parse_price

URL = "https://www.suburbia.com.mx/tienda/tenis-deportivos/catst55251553"
MAX_PRODUCTS = 100


def scrape_suburbia_selenium(project_root):
    """
    Realiza el web scraping usando Selenium y guarda los datos
    en la ruta del proyecto proporcionada.
    """
    OUTPUT_PATH = os.path.join(project_root, 'data', 'scraped_data')
    os.makedirs(OUTPUT_PATH, exist_ok=True)
    print(f"--- Scraper: Guardando datos en: {OUTPUT_PATH}")

    print("Iniciando scraping con Selenium...")

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36')

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

    products = []
    try:
        driver.get(URL)
        print(f"Página cargada: {URL}")

        wait = WebDriverWait(driver, 20)
        wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "m-product__card")))
        print("Contenedores de productos encontrados. El JavaScript ha cargado.")

        driver.execute_script("window.scrollTo(0, 1000);")
        time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'html.parser')

        product_containers = soup.find_all('li', class_='m-product__card', limit=MAX_PRODUCTS)

        if not product_containers:
            print("Error inesperado: los productos cargaron pero no se pudieron parsear.")
            return

        print(f"Procesando {len(product_containers)} productos...")

        for item in product_containers:
            brand_element = item.find('h3', class_='a-card-brand')
            desc_element = item.find('h3', class_='card-title')

            brand = brand_element.text.strip() if brand_element else ''
            description = desc_element.text.strip() if desc_element else ''
            product_name = f"{brand} {description}".strip()

            list_price_element = item.find('p', class_='a-card-price')
            discount_price_element = item.find('p', class_='a-card-discount')

            price_lista = clean_and_parse_price(list_price_element.text if list_price_element else None)
            price_descuento = clean_and_parse_price(discount_price_element.text if discount_price_element else None)

            if price_lista is None:
                price_lista = price_descuento

            if price_descuento is None:
                price_descuento = price_lista

            url_element = item.find('a', href=True)
            relative_url = url_element['href'] if url_element else None
            product_url = "https://www.suburbia.com.mx" + relative_url if relative_url else "URL no encontrada"

            sku_competidor = "SUB-" + (item.get('data-prodid') or product_name.replace(" ", "-")[:15].upper())

            products.append({
                'sku_competidor': sku_competidor,
                'nombre_producto': product_name,
                'precio_lista': price_lista,
                'precio_descuento': price_descuento,
                'url_producto': product_url,
                'fecha_extraccion': datetime.now().isoformat()
            })

    except Exception as e:
        print(f"Ha ocurrido un error durante el scraping con Selenium: {e}")

    finally:
        driver.quit()
        print("Navegador cerrado.")

    if products:
        output_file = os.path.join(OUTPUT_PATH, 'suburbia_products.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(products, f, indent=4, ensure_ascii=False)
        print(f"\n Scraping completado con éxito. Se guardaron {len(products)} productos en: {output_file}")
    else:
        print("\nNo se pudo extraer ningún producto.")


if __name__ == "__main__":
    # Esta parte es solo para pruebas aisladas
    project_root_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    scrape_suburbia_selenium(project_root_path)