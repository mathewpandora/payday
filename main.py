from dotenv import load_dotenv
from video_processing import VideoProcessor
from config.logger_config import logger
import schedule
import time
import datetime

def run_pipeline():
    try:

        logger.info(f"[{datetime.datetime.now()}] Запуск пайплайна генерации видео")
        processor = VideoProcessor()
        content = processor.generate_content()

        url, raw_video_path = processor.create_video(
            content['img_prompt'],
            content['vid_prompt'],
            duration=5
        )

        final_video_path = processor.finalize_video(
            video_path=raw_video_path,
            text=content['video_text'],
        )

        processor.upload_to_youtube(
            file_path=final_video_path,
            title=content['title'],
            description=content['description'],
            tags=content['tags']
        )

        logger.info(f"[{datetime.datetime.now()}] Пайплайн успешно завершён")

    except Exception as e:
        logger.critical(f"[{datetime.datetime.now()}] Пайплайн упал с ошибкой: {e}")
        logger.info("Ждём следующей попытки запуска завтра.")

def main():
    start_time = "05:30"
    load_dotenv()
    schedule.every().day.at(start_time).do(run_pipeline)

    logger.info("Сервис планировщика запущен, ждём запуска…")
    logger.info(f"Текущее время: {datetime.datetime.now()}")
    logger.info(f"Следующий запуск запланирован на: {start_time}")
    
    while True:
        try:
            schedule.run_pending()
            time.sleep(30)
        except Exception as e:
            logger.critical(f"[{datetime.datetime.now()}] Критическая ошибка основного цикла: {e}")
            logger.info("Основной цикл продолжает работу после ошибки.")

if __name__ == "__main__":
    main()
