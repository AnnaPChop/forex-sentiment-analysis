from alpha_vantage.foreignexchange import ForeignExchange
from dotenv import load_dotenv
import os
import pandas as pd

def get_forex_data(from_symbol='EUR', to_symbol='USD', outputsize='compact'):
    # Cargar clave API desde .env
    load_dotenv()
    api_key = os.getenv('ALPHA_VANTAGE_API_KEY')

    if not api_key:
        raise ValueError("No se encontró la clave API. Asegúrate de tener un archivo .env con ALPHA_VANTAGE_API_KEY.")

    # Inicializar cliente
    fx = ForeignExchange(key=api_key, output_format='pandas')

    # Obtener datos
    data, _ = fx.get_currency_exchange_daily(from_symbol=from_symbol, to_symbol=to_symbol, outputsize=outputsize)

    # Guardar CSV
    output_path = f'data/{from_symbol}_{to_symbol}_prices.csv'
    data.to_csv(output_path)
    print(f'Datos guardados en: {output_path}')
    return data
