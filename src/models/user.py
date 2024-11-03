from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import text, func, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models import Post
    from models import Comment


class User(Base):
    username: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text('true'))
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )

    posts: Mapped[list['Post']] = relationship(back_populates='author')
    comments: Mapped[list['Comment']] = relationship(back_populates='author')
