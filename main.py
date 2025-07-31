from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.utils.exceptions import InvalidHTTPUrlContent
import random as rd
from tools import weather, waifu, download_tiktok_video, fetch_instagram_video_url, download_video
from config import Token
import logging
import asyncio
import re
import os
from aiofiles import open as aio_open


logging.basicConfig(filename='/home/galmed/lisorybka_bot/logs/bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logging.info('Програма розпочала роботу')

bot = Bot(token=Token)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    await message.reply("Я Єбу, я сі вродив!\nТепер буду помагати пацанам в лісорубці!")


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Я вмію кликати всіх серйозних пацанів командою /all"
                        "\nрандомити число від 1 до 100 командою /roll"
                        "\nі кидати монетку командою /coin")


@dp.message_handler(commands=['all'])
async def link_all(message: types.Message):
    await message.reply("@Andrii_piro @whosvamo @Spartakusich @BMaksymko @Gabenoh")


@dp.message_handler(commands=['roll'])
async def roll(message: types.Message):
    await message.reply(str(rd.randint(1, 100)))


@dp.message_handler(commands=['coin'])
async def coin(message: types.Message):
    await message.reply(rd.choice(seq=("Орел", "Решка")))


@dp.message_handler(content_types=['sticker'])
async def send_sticker(message: types.Message):
    sticker_unique_id = str(message.sticker.file_unique_id)
    logging.info(f'{message.sticker.file_id=}')
    logging.info(f'{sticker_unique_id=}')
    if 'AgADrCYAAn986Ug' in sticker_unique_id:
        await bot.send_message(message.chat.id, "@Andrii_piro @whosvamo @Spartakusich\n@BMaksymko @Gabenoh")
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAEJGL1kbu-SQgJ9gFeXTw4iQOMVc4dHeAACrCoAAj358UjVz4vQxIJj4y8E')


async def process_and_send_video(video_url: str, message: types.Message):
    """
    Завантажує відео, надсилає його у чат та видаляє файл після цього.
    """
    save_path = "/home/galmed/lisorybka_bot/video.mp4"  # Тимчасовий файл для збереження відео

    # Завантаження відео
    await download_video(video_url, save_path)

    # Надсилання відео через Telegram
    try:
        async with aio_open(save_path, "rb") as video:
            await bot.send_video(chat_id=message.chat.id, video=video, disable_notification=True,
                                 caption=f"Надіслав @{message.from_user.username or f'користувач ID: {message.from_user.id}'}")

        print("Відео успішно відправлено!")
    except Exception as e:
        await message.reply(f"Сталася помилка під час надсилання: {str(e)}")
    finally:
        # Видалення файлу після надсилання
        if os.path.exists(save_path):
            os.remove(save_path)
            print(f"Файл {save_path} було видалено.")
        else:
            print(f"Файл {save_path} не знайдено для видалення.")


@dp.message_handler(content_types=['text'])
async def no_pon(message: types.Message):
    url_text = str(message.text)
    text = str(message.text.lower())
    b_word = ['блядь', 'блять', 'бля', 'бло']
    tiktok_url_pattern = r"(https?://)?(www\.)?(vm\.tiktok\.com/\w+|vt\.tiktok\.com/\w+|tiktok\.com/.+)"
    instagram_pattern = r"https?://(?:www\.)?instagram\.com/(?:reel|reels|share/reel)/([a-zA-Z0-9_-]+)/?"
    tik_tok_match = re.search(tiktok_url_pattern, url_text)
    instagram_match = re.search(instagram_pattern, url_text)

    # match = tik_tok_match or instagram_match
    if instagram_match:
        try:
            await process_and_send_video(await fetch_instagram_video_url(instagram_match.group()), message)
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except Exception as e:
            logging.error(e)

    if tik_tok_match:
        # await message.reply("Завантажую відео, зачекайте...")
        try:
            file_path = download_tiktok_video(tik_tok_match.group())

            # Перевірка, чи успішно завантажено файл
            if file_path is None:
                await message.reply("Не вдалося завантажити відео.")
                return

            async with aio_open(file_path, "rb") as video:
                await bot.send_video(chat_id=message.chat.id, video=video, disable_notification=True,
                                 caption=f"Надіслав @{message.from_user.username or f'користувач ID: {message.from_user.id}'}")
            logging.info(f"{file_path=}")
            logging.info("Відео успішно відправлено!")
        except Exception as e:
            await message.reply(f"Сталася помилка під час надсилання: {str(e)}")
        finally:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
            # Видалення файлу після надсилання, тільки якщо file_path не None
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                logging.info(f"Файл {file_path} було видалено.")
            else:
                logging.error(f"Файл для видалення не знайдено або не завантажено.")



    if 'пон' in text:
        text = text.lower().replace('пон', 'зроз')

    if 'бля' in text or "бло" in text:
        bed_list = [x for x in b_word if x in text]
        for i in bed_list:
            text = text.lower().replace(i, 'курва')
        if message.text.lower() != text:
            await message.reply(text.capitalize())
        else:
            await message.reply(text)

    if 'бачу' in text:
        await message.reply('Поцілуй пизду собачу')

    if 'кох' in text or 'танк' in text:
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAOeZK0CLtoc0_HNaPl9WA0BtTgbFXgAAuYqAAKK92BJX9FyadtyLNQvBA')
        await message.reply("@Andrii_piro @BMaksymko @Gabenoh @Spartakusich")

    if 'батлу' in text:
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAOfZK0C3cX3DYZAjVKFg2xeYbAVQsIAArMyAAIGk2BJnizJKURunfovBA')

    if 'пірат' in text:
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAPxZWbigD0-RaWcELGPe9t0nB8kOqsAArckAAIEJMhKmnJeTf93OEEzBA')
        await message.reply("@Andrii_piro @whosvamo @Spartakusich @Gabenoh")

    if 'русал' in text:
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAPyZWbjRgnCZyLdK0lyLnUSjZlXaHMAAoAyAAIw-WFJvq2p5elOwKozBA')

    if 'мені' in text:
        await message.reply('Дві гімні')

    if 'аніме' in text or 'anime' in text or 'тян' in text or 'дівчин' in text:
        '''
        await message.reply('Пізда тянок поки викрали!\nлови найкращу тян всіх часів і народів!')
        with open('/home/galmed/lisorybka_bot/im/1.webp', 'rb') as photo_file:
            await bot.send_photo(chat_id=message.chat.id, photo=photo_file)
        '''
        await send_waifu_image(message)

    if 'хент' in text or 'прон' in text or 'порн' in text:
        await send_waifu_image(message,is_nsfw=True)

    if 'kwad' in text or 'бобер' in text or 'квад' in text:
        try:
            with open('/home/galmed/lisorybka_bot/im/kvadrobober.jpg', 'rb') as photo_file:
                await bot.send_photo(chat_id=message.chat.id, photo=photo_file)
            await message.reply('Фурі не квадробобери')
        except Exception as e:
            logging.info(f'Помилка при виконанні запиту: {e}')

    if 'дота' in text or 'дока' in text or 'доту' in text or 'доку' in text or 'доти' in text:
        await bot.send_sticker(message.chat.id,
                               'CAACAgIAAxkBAAIBEmVtbX6iOMQ_2nT1PHEBXvquE1aUAALOJQACXTHISk7d_95TWVk9MwQ')
        await message.reply("@Andrii_piro @BMaksymko @Spartakusich @Gabenoh")

    if 'ксго' in text or 'каес' in text or 'контру' in text or 'csgo' in text or 'кс го' in text or 'го кс' in text:
            await bot.send_sticker(message.chat.id,
                                   'CAACAgIAAxkBAAIFUGbG9MNjI10y7diASU3XBBs-7ZjBAALzTwACdVo4SiNkibf6RrqnNQQ')
            await message.reply("@Andrii_piro @BMaksymko @Spartakusich @Gabenoh")

    if 'dayz' in text or 'дейзі' in text or 'дейз' in text:
                await message.reply("Загальний збір шкерів по корчам \n@whosvamo @BMaksymko @Spartakusich @Gabenoh")

    if 'бот' in text:
        await bot.send_sticker(message.chat.id,
                               'CAACAgIAAxkBAAIDkmW3Yor2nSQ-Oo6FlDQ6DMttDcrOAAKlPAACYzlxS1Ag9N0wqaMNNAQ')

    if 'валь' in text or 'вікін' in text or 'valheim' in text:
        await bot.send_sticker(message.chat.id,
                               'CAACAgIAAx0CYWKKdQACUt9mKPJJRkb50msNd6V45SvDE2dZNgACSlAAAllXQEkLlBd0sk9o8DQE')
        await link_all(message)

    if 'космос' in text or 'завод' in text or 'фактор' in text or 'факпор' in text:
        await bot.send_sticker(message.chat.id,
                               'CAACAgIAAxkBAAIFamcGJ9uOivSHvNguwttIwx9ZSK2jAAL7JgACOR1wSzI0RWtkz1qFNgQ')
        await link_all(message)

    if 'тиса' in text or 'ухилянт' in text or 'тису' in text:
        river_len, swim_len = rd.randint(120, 180), rd.randint(40, 200)
        await message.reply(f'Ухилянт {message.from_user.username} підійшов до берега Тиси, тут її ширина була '
                            f'{river_len} метрів! Голий та відчайдушний'
                            f' він зміг проплисти {swim_len} метрів до берегів Європи.')
        if swim_len < river_len:
            await bot.send_sticker(message.chat.id,
                                   'CAACAgIAAxkBAAIEvWYyK7hH3rjcVAABdszbl6ynOpynLAACZEwAAu4QiEnAQoDbVoM0-TQE')

    if 'тцк' in text or 'атб' in text:
        choice = rd.choice(("все таки зміг утекти", "ТЦК спіймало ухилянта  Press F"))
        await message.reply(f'Ухилянт {message.from_user.username} пішов в АТБ але там було ТЦК, почавши тікати'
                            f' на {rd.randint(10, 300)} метрах {choice}')
        if choice == 'ТЦК спіймало ухилянта  Press F':
            await bot.send_sticker(message.chat.id,
                                   'CAACAgIAAxkBAAIEvWYyK7hH3rjcVAABdszbl6ynOpynLAACZEwAAu4QiEnAQoDbVoM0-TQE')

    if 'фортнайт' in text or 'форточк' in text or 'дітей' in text or 'школот' in text:
        await message.reply("Їбуни дітей общий збір\n@Andrii_piro @BMaksymko @Spartakusich @Gabenoh @whosvamo")

    if 'погода' in text:
        if len(text.split(' ')) >= 2:
            city_name = text.split(' ')[text.split(' ').index('погода') + 1]
            data = await weather(city_name)
            if data is not None:
                await message.reply(
                    (f'Погода в {data["name"]}:\nТемпература: {round(float(data["main"]["temp"]) - 273.15, 0)}°C'
                     f'\nВологість: {data["main"]["humidity"]}%\n'
                     f"Стан неба: {data['weather'][0]['description']}"))
            else:
                await message.reply(f'Не знаю я такого міста {city_name}')
        else:
            await message.reply('де де тобі погоду сказати,\nнормально напиши')


async def send_waifu_image(message, is_nsfw=False):
    """
    Надсилає зображення вайфу користувачу, повторює спроби
    якщо URL невалідний.
    """
    max_attempts = 10  # Максимальна кількість спроб

    for attempt in range(max_attempts):
        try:
            # Отримати URL зображення і спробувати надіслати
            image_url = await waifu(is_nsfw)
            await message.reply_photo(image_url)
            return  # Успішне надсилання, виходимо з функції

        except InvalidHTTPUrlContent:
            # Якщо URL невалідний, чекаємо 3 секунди і пробуємо знову
            logging.error('Не вірний URL пробую ще раз')
            if attempt < max_attempts - 1:  # Якщо це не остання спроба
                await asyncio.sleep(3)

        except Exception as e:
            # Інші помилки
            logging.info(f'Помилка при надсиланні зображення: {e}')
            if attempt < max_attempts - 1:
                await asyncio.sleep(3)

    # Якщо всі спроби невдалі
    await message.reply("На жаль, не вдалося завантажити зображення тянки. Але у мене є дещо краще")
    with open('/home/galmed/lisorybka_bot/im/1.webp', 'rb') as photo_file:
        await bot.send_photo(chat_id=message.chat.id, photo=photo_file)

if __name__ == '__main__':
    executor.start_polling(dp)
    logging.info('Програма завершила роботу')
