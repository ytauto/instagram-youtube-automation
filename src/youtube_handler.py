from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
import os

class YouTubeHandler:
    def __init__(self, client_secrets_file):
        self.credentials = self.get_credentials(client_secrets_file)
        self.youtube = build('youtube', 'v3', credentials=self.credentials)

    def get_credentials(self, client_secrets_file):
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secrets_file,
            ['https://www.googleapis.com/auth/youtube.upload']
        )
        return flow.run_local_server(port=0)

    def upload_video(self, video_path, title, description):
        try:
            body = {
                'snippet': {
                    'title': title[:100],  # YouTube title limit
                    'description': description[:5000],  # YouTube description limit
                    'categoryId': '22'  # Category: People & Blogs
                },
                'status': {
                    'privacyStatus': 'public',
                    'selfDeclaredMadeForKids': False,
                }
            }

            media = MediaFileUpload(video_path, resumable=True)
            
            request = self.youtube.videos().insert(
                part='snippet,status',
                body=body,
                media_body=media
            )
            
            response = request.execute()
            return response['id']
            
        except Exception as e:
            print(f"Error uploading to YouTube: {e}")
            return None
