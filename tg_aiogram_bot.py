import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command

import tg_config

bot = Bot(token=tg_config.BOT_TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
  await message.answer(text=f"Hello? {message.from_user.full_name}!")

@dp.message(Command("help"))
async def handle_help(message: types.Message):
  text = "I'm ECHO bot.\nSend me any message!"
  entity_bold = types.MessageEntity(
    type="bold",
    offset=len("I'm ECHO bot.\nSend me "),
    length=3,
  )
  entities = [entity_bold]
  await message.answer(text=text, entities=entities)

@dp.message()
async def echo_message(message: types.Message):
  await message.answer(text="Wait a second...")

  try:
    await message.send_copy(chat_id=message.chat.id)
  except TypeError:
    await message.reply(text="Oh! Something new :)")

async def main():
  logging.basicConfig(level=logging.INFO)
  await dp.start_polling(bot)

if __name__ == "__main__":
  asyncio.run(main())