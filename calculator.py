import math

def round_down(value, decimals):
    factor = 10 ** decimals
    return math.floor(value * factor) / factor

def calculate_trade(trade_size, stop_loss_percentage, entry_price, quantity_precision, price_precision, max_leverage, risk_reward_ratio=1, side="LONG"):
    # Calcula el tamaño apalancado y el apalancamiento
    raw_quantity = trade_size / (stop_loss_percentage / 100)
    quantity = round_down(raw_quantity, quantity_precision)
    leverage = round_down(quantity / trade_size, 2)

    # Asegurar que el apalancamiento no exceda el máximo permitido
    if leverage > max_leverage:
        leverage = max_leverage

    leverage = int(leverage)

    # Calcula el precio del stop loss y take profit considerando la precisión
    if side == "LONG":
        stop_loss_price = round_down(entry_price * (1 - stop_loss_percentage / 100), price_precision)
        tp_price = round_down(entry_price * (1 + stop_loss_percentage / 100 * risk_reward_ratio), price_precision)
    else:
        stop_loss_price = round_down(entry_price * (1 + stop_loss_percentage / 100), price_precision)
        tp_price = round_down(entry_price * (1 - stop_loss_percentage / 100 * risk_reward_ratio), price_precision)

    return quantity, leverage, stop_loss_price, tp_price