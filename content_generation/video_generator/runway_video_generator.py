import os
import time
from pathlib import Path
from dotenv import load_dotenv
from runwayml import RunwayML, TaskFailedError
from content_generation.video_generator.utils import safe_filename, download_file

class RunwayVideoGenerator:
    def __init__(self, api_key: str = None):
        load_dotenv()
        self.api_key = api_key or os.getenv("RUNWAY_API_KEY")
        if not self.api_key:
            raise ValueError("Runway API key not found. Set RUNWAY_API_KEY in .env or pass it explicitly.")

        self.client = RunwayML(api_key=self.api_key)
        self.output_dir = Path("generated_videos")
        self.output_dir.mkdir(exist_ok=True)

    def generate_scene_and_video(
        self,
        image_prompt: str,
        video_prompt: str,
        duration: int = 7
    ) -> tuple[str, Path]:
        """
        Генерирует изображение, затем видео по сюжету и сохраняет видео локально.

        :param image_prompt: промпт для генерации изображения
        :param video_prompt: промпт для генерации видео
        :param duration: длительность видео в секундах
        :return: (url видео в интернете, локальный путь к видео)
        """
        ratio = "720:1280"  # минимально поддерживаемое стандартное соотношение сторон

        try:
            # Генерация изображения
            image_task = self.client.text_to_image.create(
                model="gen4_image",
                prompt_text=image_prompt,
                ratio=ratio
            ).wait_for_task_output()
        except TaskFailedError as e:
            raise RuntimeError(f"Image generation failed: {e.task_details}")

        image_url = image_task.output[0]
        print(f"[Runway] Image generated: {image_url}")

        try:
            # Генерация видео
            video_task = self.client.image_to_video.create(
                model="gen4_turbo",
                prompt_image=image_url,
                prompt_text=video_prompt,
                ratio=ratio,
                duration=duration,
            ).wait_for_task_output()
        except TaskFailedError as e:
            raise RuntimeError(f"Video generation failed: {e.task_details}")

        video_url = video_task.output[0]
        print(f"[Runway] Video generated: {video_url}")

        # Скачиваем и сохраняем видео
        filename = f"video_{int(time.time())}_{safe_filename(video_prompt)}.mp4"
        filepath = self.output_dir / filename
        download_file(video_url, filepath)
        print(f"[Runway] Video saved to: {filepath}")

        return video_url, filepath
