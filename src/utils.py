import pandas as pd
import re


def clean_and_parse_price(price_str):
  
    if price_str is None:
        return None

    # Usa una expresión regular para eliminar todo lo que no sea un dígito o un punto.
    cleaned_str = re.sub(r'[^\d.]', '', str(price_str))

    # Si después de limpiar no queda nada, retornamos None.
    if not cleaned_str:
        return None

    try:
        # Si hay un guion (rango de precios), toma el primer número
        if '-' in cleaned_str:
            cleaned_str = cleaned_str.split('-')[0]

        return float(cleaned_str)
    except (ValueError, TypeError):
        # Si algo falla en la conversión final, retornamos None.
        return None
