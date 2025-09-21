from src.domain.services.post_service import PostService
from src.domain.services.auth.authorization_service import AuthorizationService
from src.infrastructure.repositories.audience_repository import AudienceRepository
from src.domain.models.links.audience_user_link import AudienceUserLink
from src.domain.models.links.post_audience_link import PostAudienceLink
from sqlmodel import select
from typing import List

class ViewService:
    """Domain service for handling view operations and user access"""
    
    def __init__(self):
        self.post_service = PostService()
        self.authorization_service = AuthorizationService()
        self.audience_repository = AudienceRepository()
    
    async def get_view_data_for_token(self, token: str, post_id: int | None, session) -> dict:
        """Get view data based on a JWT token and optional post_id from URL"""
        payload = self.authorization_service.verify_token(token)
        if not payload:
            raise ValueError("Invalid or expired token")
        
        user_id = int(payload["sub"])
        
        if post_id:
            # User wants to view a specific post - check access and return it
            can_access = await self.authorization_service.can_user_access_post(user_id, post_id, session)
            if not can_access:
                raise PermissionError("User is not authorized to view this post")
            return await self._get_single_post_view(post_id, session)
        else:
            # User wants to see all their accessible posts
            return await self._get_user_posts_view(user_id, session)
    
    async def _get_single_post_view(self, post_id: int, session) -> dict:
        """Get a single post view"""
        post, user, _, media_items = await self.post_service.get_post_with_user_and_audiences(post_id, session)
        
        return {
            "post_id": post.id or 0,
            "description": post.description,
            "creator_name": user.name,
            "media_items": [
                {
                    "id": m.id or 0,
                    "type": m.type.value,
                    "url": f"/media-items/{m.id}/url"
                } for m in media_items
            ],
            "created_at": str(post.created_at)
        }
    
    async def _get_user_posts_view(self, user_id: int, session) -> dict:
        """Get all posts accessible to a user"""
        accessible_posts = await self._get_user_accessible_posts(user_id, session)
        return {"posts": accessible_posts}
    
    async def _get_user_accessible_posts(self, user_id: int, session) -> List[dict]:
        """Get all posts that a user can access through their audience memberships"""
        # Get all audiences the user is part of
        user_audience_links = await session.exec(
            select(AudienceUserLink).where(AudienceUserLink.user_id == user_id)
        )
        audience_ids = [link.audience_id for link in user_audience_links.all()]
        
        if not audience_ids:
            return []
        
        # Get all posts that are shared with these audiences
        all_post_links = []
        for audience_id in audience_ids:
            post_audience_links = await session.exec(
                select(PostAudienceLink)
                .where(PostAudienceLink.audience_id == audience_id)
            )
            all_post_links.extend(post_audience_links.all())
        
        post_ids = list(set([link.post_id for link in all_post_links]))  # Remove duplicates
        
        if not post_ids:
            return []
        
        # Get the actual posts with their details
        accessible_posts = []
        for post_id in post_ids:
            try:
                post, user, _, media_items = await self.post_service.get_post_with_user_and_audiences(post_id, session)
                accessible_posts.append({
                    "post_id": post.id or 0,
                    "description": post.description,
                    "creator_name": user.name,
                    "media_items": [
                        {
                            "id": m.id or 0,
                            "type": m.type.value,
                            "url": f"/media-items/{m.id}/url"
                        } for m in media_items
                    ],
                    "created_at": str(post.created_at)
                })
            except Exception:
                # Skip posts that can't be loaded
                continue
        
        # Sort posts by created_at in descending order (most recent first)
        accessible_posts.sort(key=lambda post: post["created_at"], reverse=True)
        
        return accessible_posts