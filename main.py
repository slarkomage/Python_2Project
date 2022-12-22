from aiogram.utils import executor
from create_bot import dp


async def on_startup(_):
    print("Bot online")


async def on_shutdown(_):
    print("Bot offline")


from handlers import client

client.register_handlers_client(dp)

executor.start_polling(dp, skip_updates=True, on_startup=on_startup, on_shutdown=on_shutdown)
