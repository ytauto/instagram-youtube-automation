import os
import json
from datetime import datetime
from instagram_handler import InstagramHandler
from youtube_handler import YouTubeHandler
from gpt_handler import GPTHandler
from utils import load_processed_reels, save_processed_reels, cleanup_temp

def main():
    # Initialize handlers
    instagram = InstagramHandler(
        os.environ['INSTA_USERNAME'],
        os.environ['INSTA_PASSWORD'],
        json.loads(os.environ['PROXY_LIST'])
    )
    
    youtube = YouTubeHandler('client_secrets.json')
    gpt = GPTHandler(os.environ['GPT_API_KEY'])

    # Load processed reels
    processed_reels = load_processed_reels()
    
    # Get target account's reels
    target_account = os.environ['TARGET_INSTAGRAM_ACCOUNT']
    profile = instaloader.Profile.from_username(instagram.L.context, target_account)
    
    # Process up to 3 unprocessed reels
    count = 0
    for post in profile.get_posts():
        if count >= 3:
            break
            
        if post.shortcode in processed_reels or not post.is_video:
            continue

        # Download reel
        reel_data = instagram.download_reel(post.shortcode)
        if not reel_data:
            continue

        # Process caption with GPT
        if post.caption:
            title, description = gpt.optimize_text(post.caption)
        else:
            title = reel_data['date'].strftime("%Y-%m-%d")
            description = ""

        # Upload to YouTube
        video_id = youtube.upload_video(
            reel_data['video_path'],
            title,
            description
        )

        if video_id:
            processed_reels.append(post.shortcode)
            count += 1

        # Cleanup
        cleanup_temp()

    # Save processed reels
    save_processed_reels(processed_reels)

if __name__ == "__main__":
    main()
