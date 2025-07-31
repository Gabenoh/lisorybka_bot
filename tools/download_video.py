import yt_dlp
import logging


logging.basicConfig(filename='/home/galmed/lisorybka_bot/logs/bot.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


async def download_video(video_url: str, output_path: str):
    """
    Завантажує відео за посиланням та зберігає його локально.
    """
    ydl_opts = {
        'outtmpl': output_path,
        'format': 'best[ext=mp4]',
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([video_url])
            return True
        except Exception as e:
            logging.error(f"Помилка: {e}")
            return False


if __name__ == "__main__":
    video_url = "https://scontent-mrs2-3.cdninstagram.com/o1/v/t16/f2/m86/AQPv4CBV68lVr_gaRUx5IQBzUHr3PwOaxNhGVGlmRvXoz2OcRYZlXd0PfKhhHnsJAhxAWqh9nQoh1mnobekSNJee2CcD6zO9P9sDYqM.mp4?stp=dst-mp4&efg=eyJxZV9ncm91cHMiOiJbXCJpZ193ZWJfZGVsaXZlcnlfdnRzX290ZlwiXSIsInZlbmNvZGVfdGFnIjoidnRzX3ZvZF91cmxnZW4uY2xpcHMuYzIuNzIwLmJhc2VsaW5lIn0&_nc_cat=111&vs=3872660046396591_552313053&_nc_vs=HBksFQIYUmlnX3hwdl9yZWVsc19wZXJtYW5lbnRfc3JfcHJvZC8zQzQ4ODU3ODc5OTQyNjE2ODNGM0UyMzMxMTFDOUJBRV92aWRlb19kYXNoaW5pdC5tcDQVAALIARIAFQIYOnBhc3N0aHJvdWdoX2V2ZXJzdG9yZS9HTTlqc1J3THE4N3R2V3dDQU9ncUxiMkRNeE1DYnFfRUFBQUYVAgLIARIAKAAYABsAFQAAJq7cpZGrztY%2FFQIoAkMzLBdAL5mZmZmZmhgSZGFzaF9iYXNlbGluZV8xX3YxEQB1%2Fgdl5p0BAA%3D%3D&ccb=9-4&oh=00_AfK5ZsFGGSe7JDT0TTb65BsxDDJeRvKMIV4VvbmnSt0ZDA&oe=6834F8D9&_nc_sid=10d13b"
    save_path = "test_video.mp4"
    download_video(video_url, save_path)
