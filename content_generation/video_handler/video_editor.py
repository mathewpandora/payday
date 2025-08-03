import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image, ImageColor
import subprocess
import os
from typing import Optional, Union


class VideoEditor:
    def __init__(self, video_path: str):
        self.video_path = video_path
        self.cap = cv2.VideoCapture(video_path)

        if not self.cap.isOpened():
            raise ValueError(f"Не удалось открыть видеофайл: {video_path}")

        self.fps = int(self.cap.get(cv2.CAP_PROP_FPS))
        self.width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.frame_count = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.duration = self.frame_count / self.fps

    def add_text(
        self,
        text: str,
        output_path: str = "output.mp4",
        fontsize: int = 50,
        color: str = "white",
        font_path: str = "arial.ttf",
        position: Union[str, tuple] = "center",
        duration: Optional[float] = None,
        start_time: float = 0,
        background_color: str = "black",
        padding: int = 10,
        max_width_ratio: float = 0.9
    ) -> None:
        self.cap = cv2.VideoCapture(self.video_path)

        font = ImageFont.truetype(font_path, fontsize)
        text_color = ImageColor.getrgb(color)
        bg_color = ImageColor.getrgb(background_color)

        if duration is None:
            duration = self.duration - start_time

        start_frame = int(start_time * self.fps)
        end_frame = int((start_time + duration) * self.fps)

        temp_output = "temp_no_audio.mp4"
        fourcc = cv2.VideoWriter_fourcc(*"mp4v")
        out = cv2.VideoWriter(temp_output, fourcc, self.fps, (self.width, self.height))

        frame_num = 0
        max_text_width = int(self.width * max_width_ratio)

        while True:
            ret, frame = self.cap.read()
            if not ret:
                break

            if start_frame <= frame_num <= end_frame:
                pil_img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(pil_img)

                # Автоматический перенос текста
                lines = []
                for word_line in text.split('\n'):
                    words = word_line.split()
                    current_line = ""
                    for word in words:
                        test_line = current_line + " " + word if current_line else word
                        bbox = draw.textbbox((0, 0), test_line, font=font)
                        w = bbox[2] - bbox[0]
                        if w <= max_text_width:
                            current_line = test_line
                        else:
                            lines.append(current_line)
                            current_line = word
                    if current_line:
                        lines.append(current_line)

                # Расчёт общей высоты текста по каждой строке
                text_heights = []
                for line in lines:
                    bbox = draw.textbbox((0, 0), line, font=font)
                    height = bbox[3] - bbox[1]
                    text_heights.append(height)
                total_text_height = sum(text_heights) + padding * 2 + (len(lines) - 1) * padding

                # Определение позиции (x, y)
                if isinstance(position, str):
                    if position == "center":
                        x = self.width // 2
                        y = (self.height - total_text_height) // 2
                    elif position == "top":
                        x = self.width // 2
                        y = 50
                    elif position == "bottom":
                        x = self.width // 2
                        y = self.height - total_text_height - 50
                        if y + total_text_height > self.height:
                            y = self.height - total_text_height - 10
                    else:
                        x, y = 0, 0
                else:
                    x, y = position

                # Отрисовка каждой строки
                current_y = y + padding
                for i, line in enumerate(lines):
                    text_bbox = draw.textbbox((0, 0), line, font=font)
                    text_width = text_bbox[2] - text_bbox[0]
                    text_height = text_bbox[3] - text_bbox[1]

                    text_x = x - text_width // 2
                    rect = [
                        text_x - padding,
                        current_y - padding,
                        text_x + text_width + padding,
                        current_y + text_height + padding,
                    ]
                    draw.rectangle(rect, fill=bg_color)
                    draw.text((text_x, current_y), line, font=font, fill=text_color)
                    current_y += text_height + padding

                frame = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

            out.write(frame)
            frame_num += 1

        self.cap.release()
        out.release()
        
        import shutil
        shutil.copy2(temp_output, output_path)
        os.remove(temp_output)
        print(f"✅ Видео с адаптивным текстом сохранено как {output_path}")

    def add_music(self, music_path: str, output_path: str = "output_with_music.mp4") -> None:
        cmd = [
            "ffmpeg",
            "-y",
            "-i", self.video_path,
            "-i", music_path,
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output_path
        ]

        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        if result.returncode == 0:
            print(f"🎵 Музыка успешно добавлена, сохранено в {output_path}")
        else:
            print(f"❌ Ошибка ffmpeg: {result.stderr.decode()}")

    def close(self) -> None:
        if self.cap:
            self.cap.release()
