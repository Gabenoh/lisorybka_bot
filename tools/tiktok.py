import aiohttp
from config import RAPIDAPI_HOST, RAPIDAPI_KEY
import logging


logging.basicConfig(filename='/home/galmed/lisorybka_bot/logs/bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


# Асинхронна функція для отримання інформації про відео з TikTok
async def download_tiktok_video(video_url: str):
    """
    Отримує інформацію про відео з TikTok через RapidAPI.
    Повертає посилання для завантаження відео.
    """
    api_url = "https://tiktok-video-downloader-api.p.rapidapi.com/media"
    headers = {
        "x-rapidapi-key": RAPIDAPI_KEY,
        "x-rapidapi-host": RAPIDAPI_HOST
    }
    params = {"videoUrl": video_url}

    async with aiohttp.ClientSession() as session:
        async with session.get(api_url, headers=headers, params=params) as response:
            if response.status != 200:
                error_text = await response.text()
                logging.error(f"Помилка API. Код статусу: {response.status}, Відповідь: {error_text}")
                raise Exception(f"Помилка API. Код статусу: {response.status}, Відповідь: {error_text}")

            data = await response.json()
            logging.info(f"Отримано дані: {data}")
            return data['downloadUrl']
