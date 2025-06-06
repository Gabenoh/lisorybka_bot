import aiohttp
import asyncio
import random
import logging


logging.basicConfig(filename='/home/galmed/lisorybka_bot/logs/bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def search_waifu(is_nsfw=False):
    url = 'https://api.waifu.im/search'
    if random.randint(0, 10) >= 9 or is_nsfw:
        params = {
            'height': '>=500',
            'is_nsfw': 'true'
        }
    else:
        params = {
            'height': '>=500',
            'is_nsfw': 'false'
        }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                print(params)
                response.raise_for_status()  # Перевіряємо, чи не виникла помилка при запиті
                data = await response.json()
                return data['images'][0]['url']
    except aiohttp.ClientError as e:
        logging.info(f'Помилка при виконанні запиту: {e}')
        return None


async def waifu(is_nsfw=False):
    result = await search_waifu(is_nsfw)

    if result:
        logging.info(result)
        return result
    else:
        logging.info('Не вдалося здійснити запит.')
        return None


if __name__ == "__main__":
    asyncio.run(waifu())
