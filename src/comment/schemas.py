from datetime import datetime

from pydantic import BaseModel


class CommentBaseSchema(BaseModel):
    content: str


class CommentCreateRequestSchema(CommentBaseSchema):
    post_id: int


class CommentCreateSchema(CommentCreateRequestSchema):
    user_id: int


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
    updated_at: datetime
