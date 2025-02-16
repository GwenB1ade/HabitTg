from database import session_creator
from sqlalchemy.orm import Session

from models.user import UserModel
from .base import BaseService


class UserService(BaseService):
    model = UserModel
    
    @classmethod
    def __check_user(cls, session: Session, user_telegram_id: int):
        user = session.query(cls.model).filter(
            cls.model.telegram_id == user_telegram_id
        ).first()
        
        return user if user else False
    
    @classmethod
    def create_user(
        cls,
        username: str,
        user_telegram_id: int,
    ):
        with session_creator() as s:
            check = cls.__check_user(s, user_telegram_id)
            if not check:
                user = cls.model(
                    username = username,
                    telegram_id = user_telegram_id
                )
                
                s.add(user)
                s.commit()
    
    
    @classmethod
    def get_user_by_tg_id(cls, telegram_id: int):
        with session_creator() as s:
            user = cls.__check_user(s, telegram_id)
            return user if user else False
        

    