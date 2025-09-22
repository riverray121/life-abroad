import requests
from src.utils.env import get_env_var

class SmsProvider:
    def __init__(self):
        self.api_key = get_env_var("VONAGE_API_KEY")
        self.api_secret = get_env_var("VONAGE_API_SECRET")
        self.from_number = get_env_var("SMS_FROM_NUMBER")
        
    async def send_post_notification(self, phone_number: str, user_to: str, user_from: str, post_url: str) -> dict:
        """Send SMS notification about new post"""
        message = f"Hello {user_to}! You have a new shared memory from {user_from} to view: {post_url}"

        print(f"Sending SMS to {phone_number} (from {user_from} to {user_to})")

        response = requests.post(
            'https://rest.nexmo.com/sms/json',
            data={
                'api_key': self.api_key,
                'api_secret': self.api_secret,
                'to': phone_number,
                'from': self.from_number,
                'text': message
            }
        )
        
        result = response.json()
        print(f"SMS response: {result}")
        
        if response.status_code == 200:
            print(f"SMS sent: {result.get('messages', [{}])[0].get('status', 'unknown')}")
        else:
            raise Exception(f"Failed to send SMS: {response.status_code} - {result}")
            
        return result