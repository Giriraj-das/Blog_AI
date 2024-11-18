# from fastapi import APIRouter, status, Depends
# from sqlalchemy.ext.asyncio import AsyncSession
#
# from config import settings
# from core import db_helper
# from post.schemas import PostSchema, PostsSchema, PostCreateSchema, PostUpdatePartialSchema
#
# router = APIRouter(prefix=settings.prefix.post, tags=['Posts'])
#
#
# @router.post('', response_model=PostSchema, status_code=status.HTTP_201_CREATED)
# async def create_post(
#         post_data: PostCreateSchema,
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency)
# ):
#     return await post_service.create_post(post_data=post_data)
#
#
# @router.get('', response_model=list[PostsSchema])
# async def get_posts(
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     post_service = PostService(PostCRUD(session=session))
#     return await post_service.get_posts()
#
#
# @router.get('/{post_id}', response_model=PostSchema)
# async def get_post(
#         post_id: int,
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     post_service = PostService(PostCRUD(session=session))
#     return await post_service.post_by_id(post_id=post_id)
#
#
# @router.patch("/{post_id}")
# async def update_post(
#         post_id: int,
#         post_data: PostUpdatePartialSchema,
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ):
#     post_service = PostService(PostCRUD(session=session))
#     return await post_service.update_post(
#         post_id=post_id,
#         post_data=post_data,
#         partial=True,
#     )
#
#
# @router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
# async def delete_post(
#         post_id: int,
#         session: AsyncSession = Depends(db_helper.scoped_session_dependency),
# ) -> None:
#     post_service = PostService(PostCRUD(session=session))
#     await post_service.delete_post(post_id=post_id)
