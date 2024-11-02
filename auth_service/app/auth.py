from datetime import datetime, timedelta, timezone

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.database import get_db
from app.repository import get_user
from app.schema import TokenData, User

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 90


class TokenBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(TokenBearer, self).__init__(auto_error=auto_error)

    async def __call__(
        self, request: Request, session: Session = Depends(get_db)
    ) -> HTTPAuthorizationCredentials:
        credentials = await super(TokenBearer, self).__call__(request)

        if not credentials:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authorization code.",
            )

        if not credentials.scheme == "Bearer":
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid authentication scheme.",
            )
        authentication_payload = verify_token(credentials.credentials)
        if not authentication_payload:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Invalid token or expired token.",
            )

        user_email = authentication_payload.email
        print(f"email é: {user_email}")
        if not user_email:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token missing user ID.",
            )

        user = get_user(session, email=user_email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Usuário não encontrado..",
            )

        request.state.token = credentials.credentials
        request.state.user = user

        return credentials


def create_access_token(user: User):
    to_encode = {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "birthday": user.birthday.isoformat(),
        "user_type": user.user_type.value,
    }
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str) -> TokenData | None:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_data = {
            "id": payload.get("id"),
            "username": payload.get("username"),
            "email": payload.get("email"),
            "birthday": payload.get("birthday"),
            "user_type": payload.get("user_type"),
        }

        if None in user_data.values():
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Token missing user information.",
            )

        return TokenData(**user_data)
    except JWTError as e:
        print(f"Token verification failed: {e}")
        return None  # Retorna None para indicar erro
