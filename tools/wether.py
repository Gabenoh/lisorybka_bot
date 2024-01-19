import aiohttp
import asyncio

text = 'погода Halych'
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
    api_key = '28d01a5b5da84e181577bf27a32bc5d9'
    data = await get_weather(api_key, city)
    return data


if __name__ == '__main__':
    data = asyncio.run(weather(city_name))
    print(data)
    print(f'Погода в {data["name"]}:\nТемпература: {round(float(data["main"]["temp"]) - 273.15, 0)}°C'
          f'\nВологість: {data["main"]["humidity"]}%\n'
          f"Стан неба: {data['weather'][0]['description']}")
