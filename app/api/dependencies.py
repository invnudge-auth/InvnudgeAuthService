from app.services.users import UserService


def get_user_service() -> UserService:
    return UserService()
