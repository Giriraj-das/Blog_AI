# from fastapi import HTTPException, status
#
# from comment import Comment
# from crud import CommentCRUD
# from comment.schemas import CommentCreateSchema, CommentUpdatePartialSchema
# from services import BaseService
#
#
# class CommentService(BaseService[CommentCRUD]):
#     async def create_comment(self, comment_data: CommentCreateSchema):
#         return await self.crud.create_comment(comment_data=comment_data)
#
#     async def get_comments(self):
#         return await self.crud.get_comments()
#
#     async def comment_by_id(
#             self,
#             comment_id: int,
#     ) -> Comment:
#         comment = await self.crud.get_comment(comment_id=comment_id)
#         if comment:
#             return comment
#
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail=f"Comment {comment_id} not found!",
#         )
#
#     async def update_comment(
#             self,
#             comment_id: int,
#             comment_data: CommentUpdatePartialSchema,
#             partial: bool,
#     ):
#         comment = await self.comment_by_id(comment_id=comment_id)
#         return await self.crud.update_comment(comment=comment, comment_data=comment_data, partial=partial)
#
#     async def delete_comment(self, comment_id: int):
#         comment = await self.comment_by_id(comment_id=comment_id)
#         return await self.crud.delete_comment(comment=comment)
