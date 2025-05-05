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
    # Імітуємо браузер за допомогою заголовків
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "uk,en-US;q=0.7,en;q=0.3",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": video_url,
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(video_url, headers=headers) as response:
            print(f"HTTP статус: {response.status}")  # Виводимо статус
            if response.status == 200:
                async with aiofiles.open(save_path, "wb") as f:
                    # Завантажуємо по частинах для великих файлів
                    chunk_size = 1024 * 1024  # 1MB
                    async for data in response.content.iter_chunked(chunk_size):
                        await f.write(data)
                logging.info(f"Відео завантажено: {save_path}")
                return True
            else:
                try:
                    error_text = await response.text()
                    logging.error(f"Помилка {response.status}: {error_text[:200]}")  # Обмежуємо довжину для логу
                except Exception as e:
                    logging.error(f"Помилка {response.status}: не вдалося прочитати відповідь ({str(e)})")
                return False


# if __name__ == '__main__':
#     async def test_download():
#         # URL тестового відео
#         video_url = "https://instagram.fhan5-6.fna.fbcdn.net/o1/v/t16/f2/m86/AQMo1CjQCQILegCsg6TPzaZZUIbbtlM5av4CzEHO11ayLCLaGZCuh12pD0PI0dGD-lxIJfI_mfuz_LQJVa6EXlxJzLpUbNkmVEmBNkU.mp4?stp=dst-mp4&efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuNzIwLmJhc2VsaW5lIn0&_nc_cat=107&vs=1164541191676627_2097026876&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC81NTQzMDM0REVFRjVBRjQ0MUQ3NENERDVDNDU5OUE4NV92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dIM0hMQnc1NmpqbmZrTUdBR0d5T3FVVzhyd3BicV9FQUFBRhUCAsgBACgAGAAbABUAACbiwJ%2BarLeSQBUCKAJDMywXQC8zMzMzMzMYEmRhc2hfYmFzZWxpbmVfMV92MREAdf4HAA%3D%3D&ccb=9-4&oh=00_AYAQLKuVCBj4iR6WOsov-EBbeBCyHEpB2SmGADYVSPmaZw&oe=67998397&_nc_sid=10d13b"
#         # Шлях для збереження відео
#         save_path = "test_video.mp4"
#         # Виклик функції завантаження
#         await download_video(video_url, save_path)
#
#     # Запуск тестової асинхронної функції
#     asyncio.run(test_download())


# Тестування
async def test_download():
    video_url = "https://instagram.fhan5-6.fna.fbcdn.net/o1/v/t16/f2/m86/AQMo1CjQCQILegCsg6TPzaZZUIbbtlM5av4CzEHO11ayLCLaGZCuh12pD0PI0dGD-lxIJfI_mfuz_LQJVa6EXlxJzLpUbNkmVEmBNkU.mp4?stp=dst-mp4&efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuNzIwLmJhc2VsaW5lIn0&_nc_cat=107&vs=1164541191676627_2097026876&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC81NTQzMDM0REVFRjVBRjQ0MUQ3NENERDVDNDU5OUE4NV92aWRlb19kYXNoaW5pdC5tcDQVAALIAQAVAhg6cGFzc3Rocm91Z2hfZXZlcnN0b3JlL0dIM0hMQnc1NmpqbmZrTUdBR0d5T3FVVzhyd3BicV9FQUFBRhUCAsgBACgAGAAbABUAACbiwJ%2BarLeSQBUCKAJDMywXQC8zMzMzMzMYEmRhc2hfYmFzZWxpbmVfMV92MREAdf4HAA%3D%3D&ccb=9-4&oh=00_AYAQLKuVCBj4iR6WOsov-EBbeBCyHEpB2SmGADYVSPmaZw&oe=67998397&_nc_sid=10d13b"
    # video_url = "https://robotilab.xyz/download-api/tiktok/download?videoUrl=https://www.tiktok.com/@.ciekaweciekawostki4/video/7455411872666340630"
    save_path = "test_video.mp4"
    await download_video(video_url, save_path)


if __name__ == "__main__":
    asyncio.run(test_download())
