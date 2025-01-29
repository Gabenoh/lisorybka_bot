import aiohttp
import aiofiles
import logging
import asyncio


logging.basicConfig(filename='/home/galmed/lisorybka_bot/logs/bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def download_video(video_url: str, save_path: str):
    """
    Завантажує відео за посиланням та зберігає його локально.
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(video_url) as response:
            print(response.status)
            if response.status == 200:
                async with aiofiles.open(save_path, "wb") as f:
                    await f.write(await response.read())
            else:
                logging.error('Помилка при завантаженні відео')


if __name__ == '__main__':
    async def test_download():
        # URL тестового відео
        video_url = "https://instagram.fhan5-6.fna.fbcdn.net/o1/v/t16/f2/m86/AQMo1CjQCQILegCsg6TPzaZZUIbbtlM5av4CzEHO11ayLCLaGZCuh12pD0PI0dGD-lxIJfI_mfuz_LQJVa6EXlxJzLpUbNkmVEmBNkU.mp4?stp=dst-mp4&efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuNzIwLmJhc2VsaW5lIn0&_nc_cat=107&vs=1164541191676627_2097026876&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC81NTQzMDM0REVFRjVBRjQ0MUQ3NENERDVDNDU5OUE4NV92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dIM0hMQnc1NmpqbmZrTUdBR0d5T3FVVzhyd3BicV9FQUFBRhUCAsgBACgAGAAbABUAACbiwJ%2BarLeSQBUCKAJDMywXQC8zMzMzMzMYEmRhc2hfYmFzZWxpbmVfMV92MREAdf4HAA%3D%3D&ccb=9-4&oh=00_AYAQLKuVCBj4iR6WOsov-EBbeBCyHEpB2SmGADYVSPmaZw&oe=67998397&_nc_sid=10d13b"
        # Шлях для збереження відео
        save_path = "test_video.mp4"
        # Виклик функції завантаження
        await download_video(video_url, save_path)

    # Запуск тестової асинхронної функції
    asyncio.run(test_download())
