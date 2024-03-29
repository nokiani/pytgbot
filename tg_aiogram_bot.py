import asyncio
import logging

from aiogram import Bot, F
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


@dp.message(F.photo, ~F.caption) # делаем инверсию знаком тильды. Делаем условие, если caption будет пустым
async def handle_photo_wo_caption(message: types.Message):
  await message.reply("I cannot see, sorry. Could you describe it please?")

@dp.message(F.photo, F.caption.contains("please"))
async def handle_photo_w_please_caption(message: types.Message):
  await message.reply("Do not beg me! I cannot see, sorry.")

any_media_filter = F.photo | F.video | F.document

@dp.message(any_media_filter, ~F.caption)
async def handle_any_media_wo_caption(message: types.Message):
  await message.reply("I cannot see!")

@dp.message(any_media_filter, F.caption)
async def handle_any_media_w_caption(message: types.Message):
  await message.reply(f"I can see smth is on media! It is: {message.caption!r}")

@dp.message(F.from_user.id.in_({42, 111}), F.text == "secret")
async def secret_admin_message(message: types.Message):
  await message.reply("Hi, admin!")

@dp.message()
async def echo_message(message: types.Message):
  await message.answer(
    text="Wait a second...",
    parse_mode=None,
  )

  try:
    await message.copy_to(chat_id=message.chat.id)
  except TypeError:
    await message.reply(text="Oh! Something new :)")

async def main():
  logging.basicConfig(level=logging.INFO)
  await dp.start_polling(bot)

if __name__ == "__main__":
  asyncio.run(main())