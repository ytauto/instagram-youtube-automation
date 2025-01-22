import requests

class GPTHandler:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "YOUR_GPT4_MINI_API_ENDPOINT"

    def optimize_text(self, caption):
        try:
            prompt = f"""
            Transform this Instagram caption into a YouTube title and description:
            {caption}
            
            Format:
            Title: [title]
            Description: [description]
            """
            
            response = requests.post(
                self.api_url,
                headers={"Authorization": f"Bearer {self.api_key}"},
                json={"prompt": prompt}
            )
            
            result = response.json()
            
            # Parse response to extract title and description
            lines = result['text'].split('\n')
            title = lines[0].replace('Title:', '').strip()
            description = lines[1].replace('Description:', '').strip()
            
            return title, description
        
        except Exception as e:
            print(f"Error in GPT processing: {e}")
            return caption[:100], caption  # Fallback to original caption
