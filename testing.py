from extractors import extract_type_and_ticker, extract_shock, extract_dist, extract_data
from binance_client import  place_futures_order, get_symbol_precision, get_max_leverage
from calculator import calculate_trade

message1 = """
📗LONG: ORDIUSDT📗

SHOCK: 26.947
DIST: 0.04%
TARGET: $29.733

SHOCKS
LG1: 26.947
LG2: 25.76 4.4%
LG3: 22.974 10.8%

ALL TIME HIGH
PRICE: $96.953
DIST: 258.12%
"""

type, ticker = extract_type_and_ticker(message1)
shock = extract_shock(message1)
quantity_precision, price_precision = get_symbol_precision(ticker)
max_leverage = get_max_leverage(ticker)


quantity, leverage, stop_loss_price, tp_price = calculate_trade(trade_size=5, stop_loss_percentage=2, entry_price=shock, risk_reward_ratio=1, side=type, price_precision=price_precision, quantity_precision=quantity_precision, max_leverage=max_leverage)

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

place_futures_order(symbol=ticker, entry_price=shock, quantity_dollars=quantity, tp_price=tp_price, sl_price=stop_loss_price, leverage=leverage, side=type)





