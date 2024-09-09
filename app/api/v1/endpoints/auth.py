from fastapi import APIRouter, Depends
from pydantic import BaseModel

# from app.core.security import create_access_token
from app.db.session import get_db
from sqlalchemy.orm import Session

router = APIRouter()


class LoginForm(BaseModel):
    username: str
    password: str


@router.post("/token")
def login(form_data: LoginForm, db: Session = Depends(get_db)):
    pass
    # Add actual user authentication logic here
    # user = {"sub": form_data.username}
    # access_token = create_access_token(data=user)
    # return {"access_token": access_token, "token_type": "bearer"}
