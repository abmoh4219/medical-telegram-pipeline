import asyncio
import pandas as pd
from telethon import TelegramClient
from telethon.tl.types import InputMessagesFilterPhotos
from dotenv import load_dotenv
import os
import psycopg2
from datetime import datetime

load_dotenv()

# Telegram credentials
api_id = os.getenv('TELEGRAM_API_ID')
api_hash = os.getenv('TELEGRAM_API_HASH')
phone = os.getenv('TELEGRAM_PHONE')

# PostgreSQL credentials
db_config = {
    'host': os.getenv('POSTGRES_HOST'),
    'port': os.getenv('POSTGRES_PORT'),
    'user': os.getenv('POSTGRES_USER'),
    'password': os.getenv('POSTGRES_PASSWORD'),
    'database': os.getenv('POSTGRES_DB')
}

async def scrape_channel(client, channel_username, limit=100):
    messages = []
    async for message in client.iter_messages(channel_username, limit=limit):
        msg_data = {
            'message_id': message.id,
            'channel': channel_username,
            'date': message.date,
            'text': message.text or '',
            'has_image': bool(message.photo),
            'image_path': None
        }
        if message.photo:
            image_path = f"data\\raw\\images\\{channel_username[1:]}_{message.id}.jpg"
            await message.download_media(file=image_path)
            msg_data['image_path'] = image_path
        messages.append(msg_data)
    return messages

def save_to_postgres(messages, table_name='raw_messages'):
    conn = psycopg2.connect(**db_config)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS raw_messages (
            message_id BIGINT PRIMARY KEY,
            channel VARCHAR(255),
            date TIMESTAMP,
            text TEXT,
            has_image BOOLEAN,
            image_path VARCHAR(255)
        )
    """)
    for msg in messages:
        cur.execute("""
            INSERT INTO raw_messages (message_id, channel, date, text, has_image, image_path)
            VALUES (%s, %s, %s, %s, %s, %s)
            ON CONFLICT (message_id) DO NOTHING
        """, (
            msg['message_id'], msg['channel'], msg['date'],
            msg['text'], msg['has_image'], msg['image_path']
        ))
    conn.commit()
    cur.close()
    conn.close()

async def main():
    async with TelegramClient('session_medical', api_id, api_hash) as client:
        channels = ['@CheMed123', '@lobelia4cosmetics' , '@tikvahpharma']  
        os.makedirs('data\\raw\\images', exist_ok=True)
        for channel in channels:
            messages = await scrape_channel(client, channel, limit=100)
            save_to_postgres(messages)
            pd.DataFrame(messages).to_csv(f'data\\raw\\{channel[1:]}_messages.csv', index=False)
            print(f"Scraped {len(messages)} messages from {channel}")

if __name__ == '__main__':
    asyncio.run(main())