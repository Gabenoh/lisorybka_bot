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
async def process_start_command(message: types.Message):
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

'''
@dp.message_handler(content_types=['sticker'])
async def send_sticker(message: types.Message):
    sticker_text = str(message.sticker.file_id)
    print(sticker_text)
    print('CAACAgIAAxkBAA' in sticker_text)
    print('JgACf3zpSDKGlaQ5quGLLwQ' in sticker_text)
    if 'CAACAgIAAxkBAA' in sticker_text and 'JgACf3zpSDKGlaQ5quGLLwQ' in sticker_text:
        print(message.sticker.file_id)
        await message.answer(message.sticker.file_id)
        await message.reply("@Andrii_piro @whosvamo @Spartakusich @BMaksymko @Gabenoh")
'''

if __name__ == '__main__':
    executor.start_polling(dp)
