from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
import random as rd

from config import Token

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
    if rd.randint(1, 100) > 50:
        await message.reply("Орел")
    else:
        await message.reply("Решка")


@dp.message_handler(content_types=['sticker'])
async def send_sticker(message: types.Message):
    sticker_text = str(message.sticker.file_unique_id)
    print(message.sticker.file_id)
    print(sticker_text)
    if 'AgADrCYAAn986Ug' in sticker_text:
        await bot.send_message(message.chat.id, "@Andrii_piro @whosvamo @Spartakusich\n@BMaksymko @Gabenoh")
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAEJGL1kbu-SQgJ9gFeXTw4iQOMVc4dHeAACrCoAAj358UjVz4vQxIJj4y8E')


@dp.message_handler(content_types=['text'])
async def no_pon(message: types.Message):
    text = str(message.text.lower())
    b_word = ['блядь', 'блять', 'бля', 'бло']

    if 'пон' in text:
        text = text.lower().replace('пон', 'зроз')
    if 'бл' in text:
        bed_list = [x for x in b_word if x in text]
        for i in bed_list:
            text = text.lower().replace(i, 'курва')
    if 'бачу' in text:
        await message.reply('Поцілуй пизду собачу')

    if 'кох' in text:
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAOeZK0CLtoc0_HNaPl9WA0BtTgbFXgAAuYqAAKK92BJX9FyadtyLNQvBA')
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAEJGL1kbu-SQgJ9gFeXTw4iQOMVc4dHeAACrCoAAj358UjVz4vQxIJj4y8E')
    if 'танк' in text:
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAOeZK0CLtoc0_HNaPl9WA0BtTgbFXgAAuYqAAKK92BJX9FyadtyLNQvBA')
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAEJGL1kbu-SQgJ9gFeXTw4iQOMVc4dHeAACrCoAAj358UjVz4vQxIJj4y8E')
    if 'батлу' in text:
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAOfZK0C3cX3DYZAjVKFg2xeYbAVQsIAArMyAAIGk2BJnizJKURunfovBA')
        await bot.send_sticker(message.chat.id,
                               sticker='CAACAgIAAxkBAAEJGL1kbu-SQgJ9gFeXTw4iQOMVc4dHeAACrCoAAj358UjVz4vQxIJj4y8E')

    if message.text.lower() != text:
        await message.reply(text.capitalize())


if __name__ == '__main__':
    executor.start_polling(dp)
