from content_generation.video_generator.runway_video_generator import RunwayVideoGenerator
from content_generation.promt_generator.gigachat_client import GigaChatClient
from publications.youtube_publication.youtube_connector import YouTubeConnector
from publications.youtube_publication.youtube_uploader import YouTubeUploader
from content_generation.video_handler.video_editor import VideoEditor
import os
import random
import yaml
from pathlib import Path
from typing import Dict
from config.logger_config import logger


class VideoProcessor:
    def __init__(self):
        logger.info("Initializing VideoProcessor...")
        try:
            self.giga = GigaChatClient()
            logger.info("GigaChat client initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize GigaChat client: {e}")
            raise
            
        try:
            self.generator = RunwayVideoGenerator()
            logger.info("Runway video generator initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize Runway video generator: {e}")
            raise
            
        try:
            self.youtube_connector = YouTubeConnector()
            logger.info("YouTube connector initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize YouTube connector: {e}")
            raise
            
        try:
            self.prompts = self._load_prompts()
            logger.info("Prompts loaded successfully")
        except Exception as e:
            logger.error(f"Failed to load prompts: {e}")
            raise

    def _load_prompts(self) -> Dict:
        config_path = Path(__file__).parent / "config" / "prompts.yaml"
        if not config_path.exists():
            raise FileNotFoundError(f"Config file not found at {config_path}")
        with open(config_path, 'r', encoding='utf-8') as f:
            prompts = yaml.safe_load(f)
            logger.info(f"Loaded prompts: {list(prompts.keys())}")
            logger.info(f"Available prompt types: {list(prompts['prompts'].keys())}")
            return prompts

    def generate_content(self) -> dict:
        try:
            logger.info("Starting content generation")
            logger.info(f"Available prompts: {list(self.prompts['prompts'].keys())}")

            # 1. Генерация изображения
            logger.info("Generating image prompt...")
            img_prompt = self.giga.send_prompt(self.prompts['prompts']['image_prompt'])
            logger.info(f"Сгенерированное фото: {img_prompt}")

            # 2. Генерация видео
            logger.info("Generating video prompt...")
            vid_prompt = self.giga.send_prompt(
                self.prompts['prompts']['video_prompt'].format(scene=img_prompt)
            )
            logger.info(f"Сгенерированное видео: {vid_prompt}")

            # 3. Генерация заголовка
            logger.info("Generating title...")
            context = f"{img_prompt[:300]}... {vid_prompt[:300]}..."
            logger.info(f"Context created: {context[:100]}...")
            title = self.giga.send_prompt(
                self.prompts['prompts']['title_prompt'].format(context=context)
            )
            logger.info(f"Сгенерированный заголовок: {title}")

            # 4. Генерация описания
            logger.info("Generating description...")
            description = self.giga.send_prompt(
                self.prompts['prompts']['description_prompt'].format(title=title)
            )
            logger.info(f"Сгенерированное описание: {description}")

            # 5. Генерация текста для наложения на видео
            logger.info("Generating video text...")
            video_text = self.giga.send_prompt(
                self.prompts['prompts']['video_text_prompt'].format(scene=img_prompt)
            )
            logger.info(f"Сгенерированный текст на видео: {video_text}")

            result = {
                'img_prompt': img_prompt,
                'vid_prompt': vid_prompt,
                'title': title,
                'description': description,
                'video_text': video_text,
                'tags': self.prompts['tags']
            }
            logger.info(f"Content generation completed successfully. Result keys: {list(result.keys())}")
            return result

        except Exception as e:
            logger.error(f"Content generation failed: {str(e)}")
            logger.error(f"Error type: {type(e).__name__}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            raise

    def create_video(self, img_prompt: str, vid_prompt: str, duration: int = 5) -> tuple:
        """Создание видео с логированием"""
        try:
            logger.info(f"Generating video with prompts: {img_prompt[:50]}...")
            url, path = self.generator.generate_scene_and_video(img_prompt, vid_prompt, duration)
            logger.info(f"Video generated at {path}")
            return url, path

        except Exception as e:
            logger.error(f"Video generation failed: {str(e)}")
            raise

    def upload_to_youtube(self, file_path: str, title: str, description: str, tags: list) -> dict:
        """Загрузка видео на YouTube"""
        try:
            logger.info(f"Starting YouTube upload process for video: {file_path}")

            youtube_service = self.youtube_connector.get_service()
            uploader = YouTubeUploader(youtube_service)

            response = uploader.upload_video(
                file_path=file_path,
                title=title,
                description=description,
                tags=tags,
                privacy_status="public"
            )

            logger.info(f"Video uploaded successfully! ID: {response['id']}")
            return response

        except Exception as e:
            logger.error(f"YouTube upload failed: {str(e)}")
            raise

    def finalize_video(self, video_path: str, text: str,
                       music_folder: str = "/app/content_generation/video_handler/music",
                       font_path: str = "/app/content_generation/video_handler/fonts/arialmt.ttf",
                       text_output: str = "/app/generated_videos/video_with_text.mp4",
                       final_output: str = "/app/generated_videos/final_with_music_mem.mp4") -> str:

        """
        Добавляет текст и случайную музыку из папки к видео, возвращает путь к финальному видео.
        """
        try:
            logger.info(f"Starting video finalization for: {video_path}")

            # Проверка папки и выбор случайного аудиофайла
            if not os.path.isdir(music_folder):
                raise FileNotFoundError(f"Music folder '{music_folder}' not found.")

            music_files = [f for f in os.listdir(music_folder)
                           if f.lower().endswith(('.mp3', '.wav', '.aac'))]

            if not music_files:
                raise FileNotFoundError("No audio files found in the music folder.")

            selected_music = os.path.join(music_folder, random.choice(music_files))
            logger.info(f"Selected music file: {selected_music}")

            # Добавление текста
            video_path_str = str(video_path) if hasattr(video_path, '__str__') else video_path
            editor = VideoEditor(video_path_str)
            editor.add_text(
                text=text,
                output_path=text_output,
                fontsize=35,
                color="white",
                background_color="black",
                position="bottom",
                font_path=font_path
            )

            # Добавление музыки
            editor = VideoEditor(text_output)
            editor.add_music(
                music_path=selected_music,
                output_path=final_output
            )
            editor.close()

            logger.info(f"Final video created at {final_output}")
            return str(final_output)

        except Exception as e:
            logger.error(f"Video finalization failed: {str(e)}")
            raise