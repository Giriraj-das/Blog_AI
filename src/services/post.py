from fastapi import HTTPException, status

from models import Post
from crud import PostCRUD
from schemas.post import PostCreateSchema, PostUpdatePartialSchema
from services import BaseService


class PostService(BaseService[PostCRUD]):
    async def create_post(self, post_data: PostCreateSchema):
        return await self.crud.create_post(post_data=post_data)

    async def get_posts(self):
        return await self.crud.get_posts()

    async def post_by_id(
            self,
            post_id: int,
    ) -> Post:
        post = await self.crud.get_post(post_id=post_id)
        if post:
            return post

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post {post_id} not found!",
        )

    async def update_post(
            self,
            post_id: int,
            post_data: PostUpdatePartialSchema,
            partial: bool,
    ):
        post = await self.post_by_id(post_id=post_id)
        return await self.crud.update_post(post=post, post_data=post_data, partial=partial)

    async def delete_post(self, post_id: int):
        post = await self.post_by_id(post_id=post_id)
        return await self.crud.delete_post(post=post)
