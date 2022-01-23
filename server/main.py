import secrets
from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from jose.constants import ALGORITHMS
from passlib.context import CryptContext
from pydantic import BaseModel, Field

SECRET_KEY = secrets.token_hex(32)
ALGORITHM: str = ALGORITHMS.HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 60
MY_DOMAIN = ""


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

fake_users_db = {
    "test": {
        "username": "test",
        "email": "test@example.com",
        "hashed_password": pwd_context.hash("test"),
    }
}


class Token(BaseModel):
    access_token: str
    token_type: str


class User(BaseModel):
    username: str
    email: Optional[str] = None


class UserInDB(User):
    hashed_password: str


# 参考
# https://accounts.google.com/.well-known/openid-configuration
class IdTokenResponse(BaseModel):
    # アクセストークンの有効期限。Unix エポックからの経過秒数
    exp: int = Field(...)
    # ユーザーの一意識別子
    sub: str = Field(...)
    # jwtが発行された日時。Unix エポックからの経過秒数
    iat: int = Field(...)


class IdTokenRequest(BaseModel):
    sub: str


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# tokenUrlは相対URLで指定する
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def get_user(db: dict, username: str) -> Optional[UserInDB]:
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)
    return None


def authenticate_user(
    fake_db: dict, username: str, password: str
) -> Optional[User]:
    user = get_user(fake_db, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(
    sub: str,
    expires_delta: timedelta,
    secret_key: str = SECRET_KEY,
    algorithm: str = ALGORITHM,
) -> str:
    now = datetime.utcnow()
    expire = now + expires_delta

    encoded_jwt = jwt.encode(
        IdTokenResponse(
            sub=sub,
            exp=expire.timestamp().__floor__(),
            iat=now.timestamp().__floor__(),
        ).__dict__,
        secret_key,
        algorithm=algorithm,
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        if sub is None:
            raise credentials_exception
        token_data = IdTokenRequest(sub=sub)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.sub)
    if user is None:
        raise credentials_exception
    return user


@app.post("/auth/login", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> dict:
    user = authenticate_user(
        fake_users_db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        sub=user.username,
        expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    )
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }


# デコレータ(この@hogehogeのこと)
# このデコレーターは直下の関数がオペレーション getを使用したパス/に対応することをFastAPI に通知します。
@app.get("/items/")
async def read_items(token: str = Depends(oauth2_scheme)) -> dict:
    return {"token": token}


@app.get("/users/me/", response_model=User)
async def read_users_me(
    current_user: User = Depends(get_current_user),
) -> User:
    return current_user
