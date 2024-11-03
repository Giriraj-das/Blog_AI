from datetime import datetime, timezone
from typing import TYPE_CHECKING

from sqlalchemy import func, TIMESTAMP, TEXT, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models import Base

if TYPE_CHECKING:
    from models import User
    from models import Comment


class Post(Base):
    title: Mapped[str]
    content: Mapped[str] = mapped_column(TEXT)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=datetime.now(timezone.utc),
        server_default=func.now(),
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'))

    author: Mapped['User'] = relationship(back_populates='posts')
    comments: Mapped[list['Comment']] = relationship(back_populates='post')
