from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import text, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from core.models import Post
    from core.models import Comment


class User(Base):
    username: Mapped[str] = mapped_column(unique=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text('true'))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    posts: Mapped[list['Post']] = relationship(back_populates='author')
    comments: Mapped[list['Comment']] = relationship(back_populates='author')
