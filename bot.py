from aiogram import Bot, Dispatcher, types, Router, filters, F
import asyncio
from config import API_TOKEN

bot = Bot(token=API_TOKEN)
dp = Dispatcher()
start_router = Router()

# Список команд для отображения в интерфейсе Telegram и в /help
COMMANDS_LIST = [
    ("/start", "Запустить бота"),
    ("/help", "Показать список команд"),
]

# Устанавливаем команды в интерфейс Telegram
async def set_commands(bot_instance: Bot):
    commands = [types.BotCommand(command=cmd, description=desc) for cmd, desc in COMMANDS_LIST]
    await bot_instance.set_my_commands(commands)

# Команда /start
@start_router.message(filters.CommandStart())
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я echo bot. Напиши мне что-нибудь, и я повторю.")

# Команда /help
@start_router.message(filters.Command(commands=["help"]))
async def send_help(message: types.Message):
    help_text = "Доступные команды:\n"
    for cmd, desc in COMMANDS_LIST:
        help_text += f"{cmd} — {desc}\n"
    await message.reply(help_text)

# Эхо-ответ на любой текст
@start_router.message(F.text)
async def echo(message: types.Message):
    await message.answer(f"Вы сказали: {message.text}")

# Основная функция запуска
async def main():
    await set_commands(bot)
    dp.include_router(start_router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())