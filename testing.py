from extractors import extract_type_and_ticker, extract_shock
from binance_client import   get_symbol_precision, get_max_leverage
from calculator import calculate_trade

message1 = """
📗LONG: FTMUSDT📗

SHOCK: 0.3616
DIST: 0.14%
TARGET: $0.412

SHOCKS
LG1: 0.3616
LG2: 0.3345 7.5%
LG3: 0.2841 15.1%

ALL TIME HIGH
PRICE: $3.4908
DIST: 864.04%
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

# place_futures_order(entry_price=shock, quantity_dollars=quantity, leverage=leverage, side=type, symbol=ticker)




