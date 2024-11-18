from sqlalchemy import select

from comment.crud import BaseCRUD
from models import Comment
from comment.schemas import CommentCreateSchema, CommentUpdateSchema, CommentUpdatePartialSchema


class CommentCRUD(BaseCRUD):
    async def create_comment(self, comment_data: CommentCreateSchema) -> Comment:
        comment = Comment(**comment_data.model_dump())
        self.session.add(comment)
        await self.session.commit()
        return comment

    async def get_comments(self) -> list[Comment]:
        stmt = select(Comment).order_by(Comment.id)
        result = await self.session.scalars(stmt)
        return list(result.all())

    async def get_comment(self, comment_id: int) -> Comment | None:
        return await self.session.get(Comment, comment_id)

    async def update_comment(
            self,
            comment: Comment,
            comment_data: CommentUpdateSchema | CommentUpdatePartialSchema,
            partial: bool = False,
    ) -> Comment:
        for name, value in comment_data.model_dump(exclude_unset=partial).items():
            setattr(comment, name, value)
        await self.session.commit()
        return comment

    async def delete_comment(self, comment: Comment) -> None:
        await self.session.delete(comment)
        await self.session.commit()
