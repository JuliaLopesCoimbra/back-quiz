from sqlalchemy.orm import Session
from schema.user_schema import UserCreate, TokenResponse
from service.user_service import UserService

def register_user_controller(user_data: UserCreate, db: Session) -> TokenResponse:
    user, token = UserService.create_or_enter_user(
        db,
        name=user_data.name,
        email=user_data.email
    )
    return TokenResponse(access_token=token)
