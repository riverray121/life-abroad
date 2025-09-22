from src.infrastructure.auth.jwt_provider import JwtProvider
from src.infrastructure.notifications.sms_provider import SmsProvider
from src.infrastructure.repositories.audience_repository import AudienceRepository
from src.infrastructure.repositories.post_repository import PostRepository
from src.utils.env import get_env_var

class NotificationService:
    """Domain service for handling post notifications"""
    
    def __init__(self):
        self.jwt_provider = JwtProvider()
        self.sms_provider = SmsProvider()
        self.audience_repository = AudienceRepository()
        self.post_repository = PostRepository()
    
    async def notify_audiences_of_new_post(self, post_id: int, audience_ids: list[int], session) -> None:
        """Send notifications to all users in the specified audiences about a new post"""
        if not audience_ids:
            return
        
        # Get the post creator's name
        post_creator = await self.post_repository.get_user_for_post(post_id, session)
        sender_name = post_creator.name if post_creator else "Someone"
            
        for audience_id in audience_ids:
            users = await self.audience_repository.get_users_in_audience(audience_id, session)
            for user in users:
                try:
                    # Generate authenticated link for this user with the specific post
                    token = self.jwt_provider.create_user_view_token(user.id or 0)
                    view_url = f"{get_env_var('FRONTEND_URL')}?token={token}&post_id={post_id}"
                    
                    # Send SMS notification
                    await self.sms_provider.send_post_notification(
                        user.phone_number, 
                        user.name,
                        sender_name,
                        view_url
                    )
                except Exception as e:
                    # Log error but don't fail the notification process
                    print(f"Failed to send SMS to {user.phone_number}: {e}")