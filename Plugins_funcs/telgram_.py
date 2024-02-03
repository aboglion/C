import asyncio
from telegram import Bot

async def async_telgram(CHAT_ID, TOKEN, txt, file=None):
    bot = Bot(TOKEN)
    try:
        if file:
            await bot.send_document(chat_id=CHAT_ID, caption=txt, document=open(file, 'rb'))
        else:
            await bot.send_message(chat_id=CHAT_ID, text=txt)
    except Exception as e:
        print(f"An error occurred while SENDING the message:\n {e}")

def send_via_telegram(CHAT_ID, TOKEN, txt, file=None):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    if loop.is_running():
        loop.create_task(async_telgram(CHAT_ID, TOKEN, txt, file))
    else:
        loop.run_until_complete(async_telgram(CHAT_ID, TOKEN, txt, file))
