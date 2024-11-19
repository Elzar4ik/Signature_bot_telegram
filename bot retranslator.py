from aiogram import Bot, Dispatcher, types
from aiogram.types import Message, ParseMode
from aiogram.utils import executor

# Токен бота
API_TOKEN = "8040874587:AAF81HBgxm5UI2fZhlL8KR-Hxa95qvsDp8U"

# Ініціалізація бота і диспетчера
bot = Bot(token=API_TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher(bot)

# Початковий текст, який буде додаватися до медіафайлів
added_text = "Ось ваш медіафайл із підписом!"

# Список каналів, в які додавати медіа
channels = []

# Команда /start
@dp.message_handler(commands=["start"])
async def handle_start(message: Message):
    await message.reply("Бот перезапущено! Використовуйте /help, щоб побачити доступні команди.")

# Команда /text для зміни тексту
@dp.message_handler(commands=["text"])
async def handle_text(message: Message):
    global added_text
    await message.reply("Надішліть текст із форматуванням наступним повідомленням.")

    @dp.message_handler(lambda msg: msg.text)
    async def set_text(msg: Message):
        global added_text
        added_text = msg.html_text  # Збереження тексту зі всім HTML-форматуванням
        await msg.reply(f"Новий текст збережено:\n\n{added_text}")
        dp.message_handlers.unregister(set_text)  # Видалення цього обробника після збереження тексту

# Команда /help
@dp.message_handler(commands=["help"])
async def handle_help(message: Message):
    commands = """
Список команд:
- /start - Перезапустити бота
- /text - Замінити текст, який додається до медіафайлів, надіславши новий текст наступним повідомленням
- /help - Показати список команд
- /cha_list - Показати список каналів
- /cha_add - Додати канал
    """
    await message.reply(commands)

# Команда /cha_list для показу списку каналів
@dp.message_handler(commands=["cha_list"])
async def handle_cha_list(message: Message):
    if channels:
        await message.reply("Список каналів:\n" + "\n".join(channels))
    else:
        await message.reply("Список каналів порожній.")

# Команда /cha_add для додавання каналу
@dp.message_handler(commands=["cha_add"])
async def handle_cha_add(message: Message):
    channel = message.get_args()
    if channel:
        channels.append(channel)
        await message.reply(f"Канал {channel} додано до списку.")
    else:
        await message.reply("Будь ласка, надайте посилання на канал після команди /cha_add.")

# Обробка фото
@dp.message_handler(content_types=["photo"])
async def handle_photo(message: Message):
    file_id = message.photo[-1].file_id
    existing_caption = message.caption or ""
    new_caption = f"{existing_caption}\n\n{added_text}" if existing_caption else added_text

    for channel in channels:
        await bot.send_photo(channel, file_id, caption=new_caption)

# Обробка відео
@dp.message_handler(content_types=["video"])
async def handle_video(message: Message):
    file_id = message.video.file_id
    existing_caption = message.caption or ""
    new_caption = f"{existing_caption}\n\n{added_text}" if existing_caption else added_text

    for channel in channels:
        await bot.send_video(channel, file_id, caption=new_caption)

# Обробка гіфок (анімацій)
@dp.message_handler(content_types=["animation"])
async def handle_gif(message: Message):
    file_id = message.animation.file_id
    existing_caption = message.caption or ""
    new_caption = f"{existing_caption}\n\n{added_text}" if existing_caption else added_text

    for channel in channels:
        await bot.send_animation(channel, file_id, caption=new_caption)

# Запуск бота
if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)