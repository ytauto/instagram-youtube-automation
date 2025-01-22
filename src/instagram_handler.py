import instaloader
import random
import time
from datetime import datetime
from utils import get_random_proxy

class InstagramHandler:
    def __init__(self, username, password, proxies):
        self.L = instaloader.Instaloader()
        self.proxies = proxies
        self.login(username, password)

    def login(self, username, password):
        try:
            self.L.login(username, password)
        except Exception as e:
            print(f"Login failed: {e}")
            raise

    def download_reel(self, shortcode):
        try:
            proxy = get_random_proxy(self.proxies)
            self.L.context.session.proxies = proxy
            time.sleep(random.uniform(2, 5))
            
            post = instaloader.Post.from_shortcode(self.L.context, shortcode)
            
            if not post.is_video:
                return None
            
            self.L.download_post(post, target='temp')
            
            return {
                'video_path': f'temp/{post.date_utc:%Y-%m-%d_%H-%M-%S}.mp4',
                'caption': post.caption if post.caption else post.date_utc.strftime("%Y-%m-%d"),
                'date': post.date_utc
            }
        except Exception as e:
            print(f"Error downloading reel: {e}")
            return None
