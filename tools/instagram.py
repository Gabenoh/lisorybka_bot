import aiohttp
from config import RAPIDAPI_KEY
import logging


logging.basicConfig(filename='/home/galmed/lisorybka_bot/logs/bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def fetch_instagram_video_url(instagram_url: str):
    base_url = "https://instagram-reels-downloader-api.p.rapidapi.com/download"
    # Кодуємо URL
    encoded_url = aiohttp.helpers.quote(instagram_url, safe='')

    # Формуємо повний запит
    url = f"{base_url}?url={encoded_url}"

    headers = {
        'x-rapidapi-key': RAPIDAPI_KEY,
        'x-rapidapi-host': "instagram-reels-downloader-api.p.rapidapi.com"
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as response:
            if response.status == 200:
                data = await response.text()
                print(data)
            else:
                print(f"Помилка запиту: {response.status}")
            data = await response.json()
            logging.info(f"Отримано дані: {data}")
            print(data['data']['medias'])
            print(data)
            print(f"{data['data']['medias'][0]['url']=}")
            return data['data']['medias'][0]['url']