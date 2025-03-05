import logging
import yt_dlp
import os

logging.basicConfig(filename='/home/galmed/lisorybka_bot/logs/bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def download_tiktok_video(video_url):
    """
    Завантаження відео з TikTok за допомогою yt-dlp

    :param video_url: Посилання на відео TikTok
    :return: Шлях до збереженого файлу
    """
    # Фіксований шлях та назва файлу
    save_path = "/home/galmed/lisorybka_bot/video.mp4"

    # Налаштування параметрів завантаження
    ydl_opts = {
        'format': 'mp4',
        'outtmpl': save_path
    }

    try:
        # Створення об'єкту завантаження
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Отримання інформації про відео та завантаження
            ydl.download([video_url])

            logging.info(f"Відео успішно завантажено: {save_path}")
            return save_path

    except Exception as e:
        logging.error(f"Помилка при завантаженні відео: {e}")
        return None

# Приклад використання
if __name__ == "__main__":
    print(download_tiktok_video("https://vm.tiktok.com/ZMBekoALN/"))