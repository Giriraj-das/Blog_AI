from sqlalchemy import select

from crud.base import BaseCRUD
from models import Post
from schemas.post import PostCreateSchema, PostUpdateSchema, PostUpdatePartialSchema


class PostCRUD(BaseCRUD):
    async def create_post(self, post_data: PostCreateSchema) -> Post:
        post = Post(**post_data.model_dump())
        self.session.add(post)
        await self.session.commit()
        return post

    async def get_posts(self) -> list[Post]:
        stmt = select(Post).order_by(Post.id)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_post(self, post_id: int) -> Post | None:
        return await self.session.get(Post, post_id)

    async def update_post(
            self,
            post: Post,
            post_data: PostUpdateSchema | PostUpdatePartialSchema,
            partial: bool = False,
    ) -> Post:
        for name, value in post_data.model_dump(exclude_unset=partial).items():
            setattr(post, name, value)
        await self.session.commit()
        return post

    async def delete_post(self, post: Post) -> None:
        await self.session.delete(post)
        await self.session.commit()
