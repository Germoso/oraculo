from extractors import extract_type_and_ticker, extract_shock
from binance_client import   get_symbol_precision, get_max_leverage, place_futures_order
from calculator import calculate_trade

message1 = """
📕SHORT: BTCUSDT📕

SHOCK: $59648.9
DIST: 0.07%
TARGET: $55797.9

SHOCKS
ST1: 59648.9
ST2: 61660 3.4%
ST3: 65511 6.2%

ALL TIME HIGH
PRICE: $73881.4
DIST: 23.95%
"""

type, ticker = extract_type_and_ticker(message1)
shock = extract_shock(message1)
quantity_precision, price_precision = get_symbol_precision(ticker)
max_leverage = get_max_leverage(ticker)


quantity, leverage, stop_loss_price, tp_price = calculate_trade(trade_size=2, stop_loss_percentage=2, entry_price=shock, risk_reward_ratio=1, side=type, price_precision=price_precision, quantity_precision=quantity_precision, max_leverage=max_leverage)

print("")
print("#######################")
print("Entry price:", shock)
print("Quantity:", quantity)
print("Leverage:", leverage)
print("Stop loss price:", stop_loss_price)
print("Take profit price:", tp_price)
print("Type:", type)
print("Quantity precision:", quantity_precision)
print("Price precision:", price_precision)
print("Max leverage:", max_leverage)
print("#######################")
print("")

place_futures_order(entry_price=shock, quantity_dollars=quantity, leverage=leverage, side=type, symbol=ticker)




