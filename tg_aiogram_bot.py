import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.filters import CommandStart, Command
from aiogram.utils import markdown
from aiogram.enums import ParseMode

from tg_config import settings

bot = Bot(
  token=settings.bot_token,
  # parse_mode=ParseMode.MARKDOWN_V2,
  parse_mode=ParseMode.HTML,
  )
dp = Dispatcher()

@dp.message(CommandStart())
async def handle_start(message: types.Message):
  url = "https://w7.pngwing.com/pngs/332/245/png-transparent-robot-waving-hand-bot-robot-thumbnail.png"
  await message.answer(
    text=f"{markdown.hide_link(url)}Hello, {markdown.hbold(message.from_user.full_name)}!",
    parse_mode=ParseMode.HTML,
  )

@dp.message(Command("help"))
async def handle_help(message: types.Message):
  # text = "I'm ECHO bot.\nSend me any message!"
  # entity_bold = types.MessageEntity(
  #   type="bold",
  #   offset=len("I'm ECHO bot.\nSend me "),
  #   length=3,
  # )
  # entities = [entity_bold]
  text = markdown.text(
    markdown.markdown_decoration.quote("I'm ECHO bot."),
    markdown.text(
      "Send me",
      markdown.markdown_decoration.bold(
        markdown.text(
          markdown.underline("literally"),
          "any"
        )
      ),
      markdown.markdown_decoration.quote("message!")
    ),
    sep="\n",
  )
  await message.answer(
    text=text,
    parse_mode=ParseMode.MARKDOWN_V2
  )

@dp.message(Command("code", prefix="/!%"))
async def handle_command_code(message: types.Message):
  text = markdown.text(
    "Here's Python code:",
    "",
    markdown.markdown_decoration.pre_language(
      markdown.text(
        "print('Hello world!')",
        "def foo():\n  return 'bar'",
        sep="\n"
      ),
      language="python"
    ),
    "Here's JS code:",
    "",
    markdown.markdown_decoration.pre_language(
      markdown.text(
        "console.log('Hello world!')",
        "function foo() {\n  return 'bar'\n}",
        sep="\n"
      ),
      language="javascript"
    ),
  )
  await message.answer(
    text=text,
    parse_mode=ParseMode.MARKDOWN_V2
  )


@dp.message(lambda message: message.photo)
async def handle_photo(message: types.Message):
  await message.reply("I cannot see, sorry. Could you describe it please?")

@dp.message()
async def echo_message(message: types.Message):
  await message.answer(
    text="Wait a second...",
    parse_mode=None,
  )

  try:
    # await message.forward(chat_id=message.chat.id)
    await message.copy_to(chat_id=message.chat.id)
    # await message.send_copy(chat_id=message.chat.id)
  except TypeError:
    await message.reply(text="Oh! Something new :)")

async def main():
  logging.basicConfig(level=logging.INFO)
  await dp.start_polling(bot)

if __name__ == "__main__":
  asyncio.run(main())