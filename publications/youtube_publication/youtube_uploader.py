from googleapiclient.http import MediaFileUpload
from publications.youtube_publication.utils import validate_video_file, generate_video_title
import os


class YouTubeUploader:
    def __init__(self, youtube_service):
        self.youtube = youtube_service

    def upload_video(self, file_path, title=None, description="", tags=None, privacy_status="private"):
        """Основная функция загрузки видео"""
        validate_video_file(file_path)

        if not title:
            title = generate_video_title(os.path.basename(file_path))

        body = {
            'snippet': {
                'title': title,
                'description': description,
                'tags': tags or [],
            },
            'status': {
                'privacyStatus': privacy_status,
                'selfDeclaredMadeForKids': False
            }
        }

        media = MediaFileUpload(file_path, chunksize=-1, resumable=True)

        request = self.youtube.videos().insert(
            part=",".join(body.keys()),
            body=body,
            media_body=media
        )

        return self._execute_upload(request)

    def _execute_upload(self, request):
        """Выполняет загрузку с отображением прогресса"""
        response = None
        while response is None:
            status, response = request.next_chunk()
            if status:
                print(f"Uploaded {int(status.progress() * 100)}%")

        print("Upload complete!")
        return response

    def upload_short(self, file_path, **kwargs):
        """Специализированная функция для Shorts"""
        kwargs['privacy_status'] = kwargs.get('privacy_status', 'public')
        return self.upload_video(file_path, **kwargs)