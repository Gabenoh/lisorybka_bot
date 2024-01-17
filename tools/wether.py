import aiohttp
import asyncio

text = 'погода Галич'
city_name = text.split(' ')[1]


async def get_weather(api_key, city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&lang=ua'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                print(f'Помилка при виконанні запиту: {response.status}')
                return None


async def weather(city):
    if 'галич' in city:
        city = 'Halych'
    if 'залукв' in city:
        city = 'Zalukva'
    elif 'київ' in city or 'києв' in city:
        city = 'Kyiv'
    api_key = '28d01a5b5da84e181577bf27a32bc5d9'
    data = await get_weather(api_key, city)
    return data

if __name__ == '__main__':
    asyncio.run(weather(city_name))
