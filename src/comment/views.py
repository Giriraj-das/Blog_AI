from fastapi import APIRouter, status, Depends

from comment import services
from core.config import settings
from comment.schemas import CommentSchema, CommentsSchema, CommentCreateSchema, CommentUpdatePartialSchema
from core.models import Comment

router = APIRouter(prefix=settings.prefix.comment, tags=['Comments'])


@router.post('', response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
async def create_comment(
        comment: Comment = Depends(services.create_comment)
):
    return comment


@router.get('', response_model=list[CommentsSchema])
async def get_comments_by_user(
        comments: list[Comment] = Depends(services.get_comments_by_user)
):
    return comments


@router.get('/post-comments/{post_id}', response_model=list[CommentSchema])
async def get_comments_by_post(
    comments: list[Comment] = Depends(services.get_comments_by_post)
):
    return comments


@router.get('/{comment_id}', response_model=CommentSchema)
async def get_comment_by_id(
        comment: Comment = Depends(services.get_comment_by_id)
):
    return comment


@router.patch('/{comment_id}')
async def update_comment(
        comment: Comment = Depends(services.update_comment)
):
    return comment


@router.delete(
    '/{comment_id}',
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(services.delete_comment)],
)
async def delete_comment() -> None:
    pass
