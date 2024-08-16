import os
from dotenv import load_dotenv
from binance.client import Client
from binance.exceptions import BinanceAPIException, BinanceOrderException

load_dotenv()

binance_api_key = os.getenv('B_API_KEY')
binance_api_secret = os.getenv('B_API_SECRET')

if(not binance_api_key or not binance_api_secret):
    raise ValueError("Please set your API key and secret in the .env file") 

client = Client(binance_api_key, binance_api_secret)

def get_symbol_precision(symbol):
    symbol_info = get_symbol_info(symbol)
    if symbol_info:
        # Obtén la precisión de cantidad y precio
        quantity_precision = symbol_info['quantityPrecision']
        price_precision = symbol_info['pricePrecision']
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

def place_futures_order(symbol, entry_price, quantity_dollars, tp_price, sl_price, leverage, side, margin_type="ISOLATED"):
    quantity = round(quantity_dollars / entry_price, 1)
    print(f"Placing order for {quantity} {symbol} at {entry_price} with TP at {tp_price}, SL at {sl_price}, and leverage {leverage} for {side} operation")
    
    try:
        # Establece el apalancamiento para el símbolo
        client.futures_change_leverage(symbol=symbol, leverage=leverage)

        # Cambia el tipo de margen a aislado o cruzado
        try:
            client.futures_change_margin_type(symbol=symbol, marginType=margin_type.upper())
            print(f"Tipo de margen para {symbol} establecido a {margin_type.upper()}")
        except BinanceAPIException as e:
            if e.code == -4046:  # No need to change margin type
                print(f"El tipo de margen ya está configurado como {margin_type.upper()}.")
            else:
                raise e

        # Coloca la orden en el mercado de futuros
        order = client.futures_create_order(
            symbol=symbol,
            side="SELL" if side.upper() == "SHORT" else "BUY",  # "BUY" para LONG, "SELL" para SHORT
            type='LIMIT',
            timeInForce='GTC',  # Good-Til-Canceled
            quantity=quantity,
            price=entry_price
        )
        
        print(f"Orden colocada: {order}")

        # Obtén el precio de mercado actual
        market_price = float(client.futures_mark_price(symbol=symbol)["markPrice"])

        # Validar los precios del TP y SL
        if side.upper() == "LONG":
            if tp_price <= market_price:
                raise ValueError("El precio de Take Profit para una posición LONG debe ser mayor que el precio de mercado actual.")
            if sl_price >= market_price:
                raise ValueError("El precio de Stop Loss para una posición LONG debe ser menor que el precio de mercado actual.")
        elif side.upper() == "SHORT":
            if tp_price >= market_price:
                raise ValueError("El precio de Take Profit para una posición SHORT debe ser menor que el precio de mercado actual.")
            if sl_price <= market_price:
                raise ValueError("El precio de Stop Loss para una posición SHORT debe ser mayor que el precio de mercado actual.")

        # Coloca la orden de Stop Loss
        sl_order = client.futures_create_order(
            symbol=symbol,
            side="BUY" if side.upper() == "SHORT" else "SELL",  # El SL es una operación opuesta
            type='STOP_MARKET',
            stopPrice=sl_price,  # Precio de activación del SL
            quantity=quantity,
            timeInForce='GTC'
        )
        print(f"Orden de Stop Loss colocada: {sl_order}")

        # Coloca la orden de Take Profit
        tp_order = client.futures_create_order(
            symbol=symbol,
            side="BUY" if side.upper() == "SHORT" else "SELL",  # El TP es una operación opuesta
            type='LIMIT',
            price=tp_price,  # Precio objetivo del TP
            quantity=quantity,
            timeInForce='GTC'
        )
        print(f"Orden de Take Profit colocada: {tp_order}")

    except BinanceAPIException as e:
        print(f"Error en la API de Binance: {e}")
    except BinanceOrderException as e:
        print(f"Error en la orden de Binance: {e}")
    except Exception as e:
        print(f"Otro error: {e}")
