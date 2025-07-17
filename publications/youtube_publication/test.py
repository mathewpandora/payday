from publications.youtube_publication.youtube_connector import YouTubeConnector
from publications.youtube_publication.youtube_uploader import YouTubeUploader

connector = YouTubeConnector()
youtube_service = connector.get_service()
uploader = YouTubeUploader(youtube_service)

video_path = '/Users/matvejtrofimov/Desktop/hayday/data/IMG_6636.MOV'
response = uploader.upload_video(
    file_path=video_path,
    title="My Awesome Video",
    description="This was uploaded automatically!",
    tags=["automation", "python"],
    privacy_status="public"
)
print('success')