from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import TEXT, TIMESTAMP, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models import User
    from models import Post


class Comment(Base):
    content: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))
    post_id: Mapped[int] = mapped_column(ForeignKey('posts.id'))

    author: Mapped['User'] = relationship(back_populates="comments")
    post: Mapped['Post'] = relationship(back_populates="comments")
