
from telegram import Bot
import asyncio
#pip install python-telegram-bot



async def async_telgram(CHAT_ID,TOKEN,txt,file=None):


    bot = Bot(TOKEN) 

    try:

        if file :

            await bot.send_document(chat_id=CHAT_ID, document=open(file, 'rb'))

        else:

            await bot.send_message(chat_id=CHAT_ID, text=txt) 

    except Exception as e:

        print(f"An error occurred while SENDING the message:\n {e}")

def send_via_telegram(CHAT_ID,TOKEN,txt,file=None):
    asyncio.run(async_telgram(CHAT_ID,TOKEN,txt,file))