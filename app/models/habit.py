from typing import TYPE_CHECKING
import enum
from sqlalchemy import UUID, String, Enum, ARRAY, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from datetime import time


from database import Base

if TYPE_CHECKING:
    from .user import UserModel

class DaysEnum(enum.Enum):
    Monday = 'Monday'
    Tuesday = 'Tuesday'
    Wednesday = 'Wednesday'
    Thursday = 'Thursday'
    Friday = 'Friday'
    Saturday = 'Saturday'
    Sunday = 'Sunday'

class HabitModel(Base):
    __tablename__ = 'Habit'
    uuid: Mapped[str] = mapped_column(UUID(as_uuid = False), primary_key = True, default = uuid.uuid4)
    title: Mapped[str] = mapped_column(String(length = 50))
    desc: Mapped[str] = mapped_column(nullable = True)
    time: Mapped[time]
    days: Mapped[list[str]] = mapped_column(ARRAY(Enum(DaysEnum)))
    
    user: Mapped['UserModel'] = relationship(
        back_populates = 'habits',
        uselist = False
    )
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id', ondelete='CASCADE'))