from extractors import extract_type_and_ticker, extract_shock, extract_dist, extract_data
from binance_client import  place_futures_order, get_max_leverage, get_symbol_precision
from telethon import TelegramClient, events
from calculator import calculate_trade
from telethon import TelegramClient
from dotenv import load_dotenv
import os

load_dotenv()

api_id = os.getenv('T_API_ID')
api_hash = os.getenv('T_API_HASH')
phone_number = os.getenv('T_PHONE_NUMBER')

# Inicia el cliente de Telegram
client = TelegramClient('session_name', api_id, api_hash)

target = 'BtcxalertsBot'

@client.on(events.NewMessage)
async def my_event_handler(event):
    sender = await event.get_sender()
    sender_name = sender.username if sender.username else sender.id
    message_text = event.message.message

    print(f'Mensaje de {sender_name}: {message_text}')

    if sender_name == target:
        trade_type, ticker = extract_type_and_ticker(message_text)
        shock = extract_shock(message_text)
        dist = extract_dist(message_text)

        if trade_type and ticker and shock is not None and dist is not None:
            print(f'Extraído: Tipo: {trade_type}, Ticker: {ticker}, Shock: {shock}, Dist: {dist}%')

            ########################

            type, ticker = extract_type_and_ticker(message_text)
            shock = extract_shock(message_text)
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

            place_futures_order(symbol=ticker, entry_price=shock, quantity_dollars=quantity, tp_price=tp_price, sl_price=stop_loss_price, leverage=50, side=type)

            ########################

            await client.send_message('me', f'trade_type: {trade_type}, ticker: {ticker}, shock: {shock}, dist: {dist}%')


# Inicia la sesión de Telegram
async def main():
    await client.start(phone_number)
    print("Cliente iniciado.")
    await client.send_message('me', f'Bot en marcha')

    await client.run_until_disconnected()

with client:
    client.loop.run_until_complete(main())
