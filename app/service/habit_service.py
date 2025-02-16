from models.user import UserModel
from models.habit import HabitModel, DaysEnum
from .base import BaseService
from .user_service import UserService
from database import session_creator

class HabitService(BaseService):
    model = HabitModel
    user_services = UserService
    
    @classmethod
    def create_habit(
        cls,
        telegram_id: int,
        title: str,
        time: str,
        days: list
    ):
        with session_creator() as s:
            user = cls.user_services.get_user_by_tg_id(telegram_id)
            habit = HabitModel(
                title = title,
                time = time,
                days = [DaysEnum(day.capitalize()) for day in days],
            )
            habit.user = user
            
            s.add(habit)
            s.commit()
            
            return habit
    
    
    @classmethod
    def get_habits(
        cls,
        telegram_id: int,
        skip: int = 0,
        limit: int = 5
    ) -> list[HabitModel]:
        with session_creator() as s:
            user = s.query(UserModel).filter_by(telegram_id = telegram_id).first()
            
            habits = []
            for i in range(skip, limit + skip):
                try:
                    habits.append(user.habits[i])
                
                except:
                    break
            return habits
    
    
    @classmethod
    def get_one_habit(
        cls,
        habit_id: str
    ) -> HabitModel:
        with session_creator() as s:
            habit = s.query(cls.model).filter(
                cls.model.uuid == habit_id
            ).first()
            
            return habit
        
    
    @classmethod
    def delete_habit(
        cls,
        habit_id: str
    ) -> 'HabitModel':
        with session_creator() as s:
            habit = s.query(cls.model).filter(
                cls.model.uuid == habit_id
            ).first()
            
            s.query(cls.model).filter(
                cls.model.uuid == habit_id
            ).delete()
            
            s.commit()
            
            return habit
    
    @classmethod
    def get_all_habits(cls) -> list['HabitModel']:
        with session_creator() as s:
            habits = s.query(cls.model).all()
            for h in habits:
                user = h.user
            return habits
    