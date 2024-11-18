from datetime import datetime

from pydantic import BaseModel


class CommentBaseSchema(BaseModel):
    content: str


class CommentCreateSchema(CommentBaseSchema):
    user_id: int
    post_id: int


class CommentUpdateSchema(CommentBaseSchema):
    pass


class CommentUpdatePartialSchema(CommentBaseSchema):
    content: str | None = None


class CommentsSchema(CommentBaseSchema):
    id: int


class CommentSchema(CommentsSchema):
    user_id: int
    post_id: int
    created_at: datetime
