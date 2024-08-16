from extractors import extract_type_and_ticker, extract_shock
from calculator import calculate_trade

 ################### EXTRAER DATOS #####################

message = """
📕SHORT: BTCUSDT📕

SHOCK: $60839.1
DIST: 0.01%
TARGET: $57788.1

SHOCKS
ST1: 60839.1
ST2: 62278 2.4%
ST3: 65329 4.9%

ALL TIME HIGH
PRICE: $73881.4
DIST: 21.43%
"""

type, ticker = extract_type_and_ticker(message)
shock = extract_shock(message)

quantity, leverage, stop_loss_price, tp_price = calculate_trade(trade_size=5, stop_loss_percentage=2, entry_price=shock, risk_reward_ratio=1, side=type)

print("Quantity:", quantity)
print("Leverage:", leverage)
print("Stop loss price:", stop_loss_price)
print("Take profit price:", tp_price)
print("Type:", type)

# Quantity: 250.0
# Leverage: 50.0
# Stop loss price: 62055.882
# Take profit price: 59622.318
# Type: SHORT


























# client = Client(api_key=binance_api_key, api_secret=binance_api_secret)

# # Descargar datos históricos de velas (Kline)
# candles = client.get_historical_klines("BTCUSDT", Client.KLINE_INTERVAL_1DAY, "1 Jan, 2020", "1 Jan, 2023")

# # Guardar los datos en un CSV
# import pandas as pd
# df = pd.DataFrame(candles, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base', 'taker_buy_quote', 'ignore'])
# df.to_csv('BTCUSDT_data.csv', index=False)

import pandas as pd

# Cargar los datos históricos
df = pd.read_csv('BTCUSDT_data.csv')

# Convertir el timestamp a un formato de fecha que backtrader pueda entender
df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')

# Renombrar columnas para que coincidan con el formato esperado por backtrader
df = df.rename(columns={'timestamp': 'datetime', 'open': 'Open', 'high': 'High', 'low': 'Low', 'close': 'Close', 'volume': 'Volume'})

# Establecer la columna datetime como índice
df.set_index('datetime', inplace=True)

# Guardar en un CSV para cargarlo en backtrader
df.to_csv('BTCUSDT_backtrader.csv')










import pandas as pd

# Leer los datos históricos
df = pd.read_csv('BTCUSDT_data.csv', parse_dates=['timestamp'])

# Lista de entradas simuladas
entries = [
    {'entry': 60839.1, 'stop_loss': 62055.882, 'take_profit': 59622.318, 'type': 'SHORT'},
    # Agrega más entradas según sea necesario
]

# Resultado de las operaciones
results = []

for entry in entries:
    entry_price = entry['entry']
    stop_loss = entry['stop_loss']
    take_profit = entry['take_profit']
    trade_type = entry['type']
    
    if trade_type == 'SHORT':
        entry_signal = df[df['high'] >= entry_price]
        if not entry_signal.empty:
            entry_index = entry_signal.index[0]
            data_after_entry = df.iloc[entry_index:]
            
            # Verificar si alcanza el stop loss o take profit primero
            sl_hit = data_after_entry[data_after_entry['high'] >= stop_loss]
            tp_hit = data_after_entry[data_after_entry['low'] <= take_profit]
            
            if not sl_hit.empty and not tp_hit.empty:
                sl_index = sl_hit.index[0]
                tp_index = tp_hit.index[0]
                
                if tp_index < sl_index:
                    results.append({'entry': entry_price, 'result': 'Take Profit', 'exit_price': take_profit})
                else:
                    results.append({'entry': entry_price, 'result': 'Stop Loss', 'exit_price': stop_loss})
            elif not sl_hit.empty:
                results.append({'entry': entry_price, 'result': 'Stop Loss', 'exit_price': stop_loss})
            elif not tp_hit.empty:
                results.append({'entry': entry_price, 'result': 'Take Profit', 'exit_price': take_profit})
            else:
                results.append({'entry': entry_price, 'result': 'Open Position', 'exit_price': None})

    elif trade_type == 'LONG':
        entry_signal = df[df['low'] <= entry_price]
        if not entry_signal.empty:
            entry_index = entry_signal.index[0]
            data_after_entry = df.iloc[entry_index:]
            
            # Verificar si alcanza el stop loss o take profit primero
            sl_hit = data_after_entry[data_after_entry['low'] <= stop_loss]
            tp_hit = data_after_entry[data_after_entry['high'] >= take_profit]
            
            if not sl_hit.empty and not tp_hit.empty:
                sl_index = sl_hit.index[0]
                tp_index = tp_hit.index[0]
                
                if tp_index < sl_index:
                    results.append({'entry': entry_price, 'result': 'Take Profit', 'exit_price': take_profit})
                else:
                    results.append({'entry': entry_price, 'result': 'Stop Loss', 'exit_price': stop_loss})
            elif not sl_hit.empty:
                results.append({'entry': entry_price, 'result': 'Stop Loss', 'exit_price': stop_loss})
            elif not tp_hit.empty:
                results.append({'entry': entry_price, 'result': 'Take Profit', 'exit_price': take_profit})
            else:
                results.append({'entry': entry_price, 'result': 'Open Position', 'exit_price': None})

# Imprimir los resultados
for result in results:
    print(result)
