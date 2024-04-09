from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import random as rd
from tools import weather, waifu
from config import Token
import logging

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
    await message.reply(rd.choice("Орел", "Решка"))


@dp.message_handler(content_types=['sticker'])
async def send_sticker(message: types.Message):
    sticker_unique_id = str(message.sticker.file_unique_id)
    logging.info(f'{message.sticker.file_id=}')
    logging.info(f'{sticker_unique_id=}')
    if 'AgADrCYAAn986Ug' in sticker_unique_id:
        await bot.send_message(message.chat.id, "@Andrii_piro @whosvamo @Spartakusich\n@BMaksymko @Gabenoh")
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAEJGL1kbu-SQgJ9gFeXTw4iQOMVc4dHeAACrCoAAj358UjVz4vQxIJj4y8E')


@dp.message_handler(content_types=['text'])
async def no_pon(message: types.Message):
    text = str(message.text.lower())
    b_word = ['блядь', 'блять', 'бля', 'бло']

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

    if 'аніме' in text or 'anime' in text or 'тян' in text or 'дівчин' in text:
        '''
        await message.reply('Пізда тянок поки викрали!\nлови найкращу тян всіх часів і народів!')
        with open('/home/galmed/lisorybka_bot/im/1.webp', 'rb') as photo_file:
            await bot.send_photo(chat_id=message.chat.id, photo=photo_file)

        '''
        image_url = await waifu()
        try:
            await message.reply_photo(image_url)
        except Exception as e:
            logging.info(f'Помилка при виконанні запиту: {e}')
            image_url = await waifu()
            await message.reply_photo(image_url)

    if 'хент' in text or 'прон' in text or 'порн' in text:
        image_url = await waifu(is_nsfw=True)
        try:
            await message.reply_photo(image_url)
        except Exception as e:
            logging.info(f'Помилка при виконанні запиту: {e}')
            image_url = await waifu(is_nsfw=True)
            await message.reply_photo(image_url)

    if 'дота' in text or 'дока' in text or 'доту' in text or 'доку' in text:
        await bot.send_sticker(message.chat.id,
                               'CAACAgIAAxkBAAIBEmVtbX6iOMQ_2nT1PHEBXvquE1aUAALOJQACXTHISk7d_95TWVk9MwQ')
        await message.reply("@Andrii_piro @BMaksymko @Spartakusich @Gabenoh")

    if 'бот' in text:
        await bot.send_sticker(message.chat.id,
                               'CAACAgIAAxkBAAIDkmW3Yor2nSQ-Oo6FlDQ6DMttDcrOAAKlPAACYzlxS1Ag9N0wqaMNNAQ')

    if 'тис' in text or 'ухилянт' in text:
        await message.reply(f'Ухилянт {message.from_user.username} підійшов до берега Тиси, тут її ширина була '
                            f'{rd.randint(120, 180)} метрів! Голий та відчайдушний'
                            f' він зміг проплисти {rd.randint(40, 200)} метрів до берегів Європи.')

    if 'тцк' in text or 'атб' in text:
        await message.reply(f'Ухилянт {message.from_user.username} пішов в АТБ але там було ТЦК, почавши тікати'
                            f' на {rd.randint(10, 300)} метрах {rd.choice(("все таки зміг утекти", "ТЦК спіймало ухилянта  Press F"))}')

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


if __name__ == '__main__':
    executor.start_polling(dp)
    logging.info('Програма завершила роботу')
