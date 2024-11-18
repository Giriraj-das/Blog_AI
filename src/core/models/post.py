from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import func, TIMESTAMP, TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.models import Base

if TYPE_CHECKING:
    from core.models import User
    from core.models import Comment


class Post(Base):
    title: Mapped[str]
    content: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    author: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[list['Comment']] = relationship(back_populates='post', cascade='all, delete-orphan')
