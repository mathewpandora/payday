import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request


class YouTubeConnector:
    def __init__(self, client_secret_file='publications/youtube_publication/client_secret_439707286940-5qe8kh3tit3ia9rrg9nufjgndug21lkd.apps.googleusercontent.com.json', token_file='publications/youtube_publication/token.json'):
        self.client_secret_file = client_secret_file
        self.token_file = token_file
        self.scopes = ['https://www.googleapis.com/auth/youtube.upload']
        self.service = self._authenticate()

    def _authenticate(self):
        creds = None

        if os.path.exists(self.token_file):
            creds = Credentials.from_authorized_user_file(self.token_file, self.scopes)

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.client_secret_file,
                    self.scopes,
                    redirect_uri='http://localhost:8080'  # Явно указываем порт
                )
                creds = flow.run_local_server(port=8080)  # Используем тот же порт

            with open(self.token_file, 'w') as token:
                token.write(creds.to_json())

        return build('youtube', 'v3', credentials=creds)

    def get_service(self):
        return self.service