from typing import TYPE_CHECKING
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey
from database import Base

if TYPE_CHECKING:
    from .habit import HabitModel

class UserModel(Base):
    __tablename__ = 'User'
    id: Mapped[int] = mapped_column(primary_key = True)
    telegram_id: Mapped[int]
    username: Mapped[str]
    
    habits: Mapped[list['HabitModel']] = relationship(
        back_populates = 'user',
        uselist = True
    )
    