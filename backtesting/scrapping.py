from telethon import TelegramClient
import json
import os
from dotenv import load_dotenv

load_dotenv()

api_id = os.getenv('T_API_ID')
api_hash = os.getenv('T_API_HASH')
phone_number = os.getenv('T_PHONE_NUMBER')

if(not api_id or not api_hash or not phone_number):
    raise ValueError("Please set your API key and secret in the .env file") 

target = 'BtcxalertsBot'

  # Inicializa el cliente de Telethon
client = TelegramClient('scrapping', api_id, api_hash)

async def main():
    # Conéctate al cliente
    await client.start(phone_number)
    print("Cliente iniciado.")
    
    # Reemplaza 'target' con el nombre de usuario o ID del canal que deseas leer
    channel = await client.get_entity(target)
    print(f"Obteniendo mensajes del canal {target}...")
    
    # Obtener todos los mensajes del canal
    messages = []
    async for message in client.iter_messages(channel):
        messages.append({
            'id': message.id,
            'sender_id': message.sender_id,
            'date': message.date.isoformat(),
            'text': message.text
        })

    # Guardar los mensajes en un archivo JSON
    with open('messages.json', 'w') as f:
        json.dump(messages, f, indent=4)

    print(f"Mensajes guardados en 'messages.json'")

# Ejecutar el script
with client:
    client.loop.run_until_complete(main())