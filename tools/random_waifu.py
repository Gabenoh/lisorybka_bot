import aiohttp
import asyncio


async def search_waifu():
    url = 'https://api.waifu.im/search'
    params = {
        'height': '>=1000',
        'is_nsfw': 'null'
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                response.raise_for_status()  # Перевіряємо, чи не виникла помилка при запиті
                data = await response.json()
                return data['images'][0]['url']
    except aiohttp.ClientError as e:
        print(f'Помилка при виконанні запиту: {e}')
        return None


async def waifu():
    result = await search_waifu()

    if result:
        # Обробляємо результат за потреби
        print(result)
        return result
    else:
        print('Не вдалося здійснити запит.')


if __name__ == "__main__":
    asyncio.run(waifu())
