from dotenv import load_dotenv
from video_processing import VideoProcessor
from config.logger_config import logger

def main():
    load_dotenv()
    try:
        logger.info("Starting video generation pipeline")

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

        logger.info("Pipeline completed successfully")

    except Exception as e:
        logger.critical(f"Pipeline failed: {str(e)}")
        raise

if __name__ == "__main__":
    main()


"""
Текст к видео - полный пиздец... нужно нормально настроить промпты
удалить лишние папки с контентом - нормально нстроить папки с контентом
добавить вк
сделать нормальную работу с путями (к музыке в файлам и так далее)
прромпты отдельно настроить
"""