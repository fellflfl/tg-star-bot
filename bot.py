import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

# ================= НАСТРОЙКИ =================
BOT_TOKEN = "9212369160:AAEi5XENA3U8X9V6rqmti8gaqktTCHboSL8"
WEBAPP_URL = "https://wlqpv-80-244-42-178.run.pinggy-free.link "
# =============================================

dp = Dispatcher()

@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(
                text="🚀 Открыть Кейсы и Апгрейдер",
                web_app=WebAppInfo(url=WEBAPP_URL)
            )
        ]
    ])
    await message.answer(
        f"Привет, <b>{message.from_user.first_name}</b>! ⭐\n\n"
        "Добро пожаловать в мини-приложение:\n"
        "• 🎁 Забирай <b>+20 000 звезд</b> каждую минуту в профиле\n"
        "• 📦 Открывай кейсы за 1к, 5к и 10к звезд\n"
        "• ⚡ Прокачивай выбитые предметы в Апгрейдере!",
        reply_markup=kb,
        parse_mode="HTML"
    )

async def serve_index(request):
    file_path = os.path.join(os.path.dirname(__file__), "index.html")
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    return web.Response(text=html_content, content_type="text/html", charset="utf-8")

async def main():
    app = web.Application()
    app.router.add_get("/", serve_index)
    runner = web.AppRunner(app)
    await runner.setup()

    # Порт для Render или локального ПК
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"✅ Сервер запущен на порту {port}")
    # 2. Пробуем запустить Telegram-бота
    try:
        bot = Bot(token=BOT_TOKEN)
        print("⏳ Подключаемся к серверам Telegram...")
        await dp.start_polling(bot)
    except Exception as e:
        print(f"\n❌ Бот не смог подключиться к Telegram: {e}")
        print("⚠️ Но локальный сайт продолжает работать на http://127.0.0.1:8080 !")
        # Держим сервер открытым, чтобы сайт не выключался
        while True:
            await asyncio.sleep(3600)

if __name__ == "__main__":
    asyncio.run(main())