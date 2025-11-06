from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, date
from jose import jwt, JWTError
import os

# Create all tables
models.Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# OAuth2 token URL
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Path to the frontend dist directory
frontend_dist_dir = os.path.join(os.path.dirname(__file__), 'frontend', 'dist')

# Serve static frontend files if built (check for 'frontend/dist' directory)
if os.path.isdir(frontend_dist_dir):
    app.mount('/', StaticFiles(directory=frontend_dist_dir, html=True), name='static')

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post('/token', response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    access_token_expires = timedelta(minutes=60*24)
    access_token = auth.create_access_token(data={'sub': user.username, 'role': user.role}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

@app.post('/users', response_model=dict)
d
