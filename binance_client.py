import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

load_dotenv()

binance_api_key = os.getenv('B_API_KEY')
binance_api_secret = os.getenv('B_API_SECRET')

if not binance_api_key or not binance_api_secret:
    raise ValueError("Please set your API key and secret in the .env file")

client = Client(binance_api_key, binance_api_secret)

def round_price_to_tick_size(price, tick_size):
    return round(price / tick_size) * tick_size

def round_quantity_to_precision(quantity, precision):
    return round(quantity, precision)

def get_symbol_precision(symbol):
    symbol_info = get_symbol_info(symbol)
    print(symbol_info)
    if symbol_info:
        # Obtén la precisión de cantidad y precio
        quantity_precision = symbol_info['baseAssetPrecision']
        price_precision = symbol_info['quantityPrecision']
        return quantity_precision, price_precision
    else:
        return None, None

def get_symbol_info(symbol):
    try:
        # Obtener información del símbolo
        info = client.futures_exchange_info()
        symbol_info = next(item for item in info['symbols'] if item['symbol'] == symbol)
        return symbol_info
    except BinanceAPIException as e:
        print(f'Error al obtener información del símbolo: {e}')
        return None

def get_max_leverage(symbol):
    try:
        info = client.futures_leverage_bracket()
        for item in info:
            if item['symbol'] == symbol:
                return item['brackets'][0]['initialLeverage']
        return None
    except BinanceAPIException as e:
        print(f'Error al obtener el apalancamiento máximo: {e}')
        return None

def place_futures_order(symbol, entry_price, quantity_dollars, leverage, side, margin_type="CROSSED"):
    # Obtener el tick size y la precisión de cantidad para el símbolo
    tick_size, quantity_precision = get_symbol_precision(symbol)
    if tick_size is None or quantity_precision is None:
        print(f"No se pudo obtener el tick size o la precisión para {symbol}.")
        return

    # Ajustar precios y cantidad a los valores correctos
    quantity = round(quantity_dollars / entry_price, quantity_precision)

    try:
        # Cambiar el apalancamiento
        client.futures_change_leverage(symbol=symbol, leverage=leverage)
        
        # Cambiar el tipo de margen
        try:
            client.futures_change_margin_type(symbol=symbol, marginType=margin_type.upper())
            print(f"Tipo de margen para {symbol} establecido a {margin_type.upper()}")
        except BinanceAPIException as e:
            if e.code == -4046:
                print(f"El tipo de margen ya está configurado como {margin_type.upper()}.")
            else:
                raise e

        print(f"Creando orden de {side} para {quantity} {symbol} a {entry_price}")

        order = client.futures_create_order(
            symbol=symbol,
            side="SELL" if side.upper() == "SHORT" else "BUY",
            type='LIMIT',
            timeInForce='GTC',
            quantity=quantity,
            price=entry_price
        )
        
        print(f"Orden colocada: {order}")

    except BinanceAPIException as e:
        print(f"Error en la API de Binance: {e}")
    except BinanceOrderException as e:
        print(f"Error en la orden de Binance: {e}")
    except Exception as e:
        print(f"Otro error: {e}")
