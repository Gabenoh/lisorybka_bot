import aiohttp
import asyncio
import random
import logging


logging.basicConfig(filename='/home/galmed/lisorybka_bot/logs/bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def search_waifu(IsNsfw=False):
    url = 'https://api.waifu.im/images'
    if random.randint(0, 10) >= 9 or IsNsfw:
        params = {
            'height': '>=500',
            'IsNsfw': 'true'
        }
    else:
        params = {
            'height': '>=500',
            'IsNsfw': 'false'
        }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                print(params)
                response.raise_for_status()  # Перевіряємо, чи не виникла помилка при запиті
                data = await response.json()
                return data['items'][0]['url']
    except aiohttp.ClientError as e:
        logging.info(f'Помилка при виконанні запиту: {e}')
        return None


async def waifu(IsNsfw=False):
    result = await search_waifu(IsNsfw)

    if result:
        logging.info(result)
        return result
    else:
        logging.info('Не вдалося здійснити запит.')
        return None


if __name__ == "__main__":
    asyncio.run(waifu())
