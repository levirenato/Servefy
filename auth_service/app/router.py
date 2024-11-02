from fastapi import APIRouter, Depends, HTTPException, Request, status
from app.repository import create_user, create_log, get_user
from app.schema import (
    User,
    UserCreate,
    Token,
    UserLogin,
)
from app.database import get_db
from app.auth import TokenBearer, create_access_token, verify_token
import time
from passlib.context import CryptContext

router = APIRouter(dependencies=[Depends(get_db)])
router_private = APIRouter(dependencies=[Depends(TokenBearer())])
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@router.post("/register", response_model=User)
def register(user: UserCreate, db: Request) -> User:
    user.password = pwd_context.hash(user.password)
    new_user = create_user(db.state.session, user)
    create_log(db.state.session, "user_registered", str(new_user.email), time.time())
    return new_user


@router.post("/login", response_model=Token)
def login(form_data: UserLogin, db: Request) -> Token:
    db_user = get_user(
        db.state.session, email=form_data.email
    )  # Buscando usuário diretamente
    if not db_user or not pwd_context.verify(
        form_data.password, str(db_user.hashed_password)
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Se o usuário foi encontrado e a senha é válida
    access_token = create_access_token(user=db_user)
    create_log(db.state.session, "user_logged_in", str(db_user.email), time.time())
    return Token(access_token=access_token, token_type="bearer")


@router_private.get("/users/me", response_model=User)
def read_users_me(db: Request):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    # Verifique se está passando o token em vez do objeto `User`
    token = db.state.token  # Suponha que você armazene o token em `db.state.token`

    if not token:
        raise credentials_exception

    token_data = verify_token(token)  # Passe o token aqui, não o usuário

    if not token_data:
        raise credentials_exception

    user = db.state.user
    if user is None:
        raise credentials_exception

    return user


router.include_router(router_private)
