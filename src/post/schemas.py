from datetime import datetime

from pydantic import BaseModel


class PostBaseSchema(BaseModel):
    title: str
    content: str


class PostCreateSchema(PostBaseSchema):
    user_id: int


class PostUpdateSchema(PostBaseSchema):
    pass


class PostUpdatePartialSchema(PostBaseSchema):
    title: str | None = None
    content: str | None = None


class PostsSchema(PostBaseSchema):
    id: int


class PostSchema(PostsSchema):
    user_id: int
    created_at: datetime
