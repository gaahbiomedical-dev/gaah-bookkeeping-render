from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, date
from jose import jwt, JWTError
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os

from . import models, schemas, crud, auth
from .database import SessionLocal, engine

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# ---------------- FRONTEND SERVING (IMPORTANT) ---------------- #

# Path to dist folder (one level above app/)
frontend_dist = os.path.join(os.path.dirname(os.path.dirname(__file__)), "dist")

# Serve static asset files (js/css)
app.mount("/assets", StaticFiles(directory=os.path.join(frontend_dist, "assets")), name="assets")

# Serve index.html on root
@app.get("/")
def serve_frontend():
    return FileResponse(os.path.join(frontend_dist, "index.html"))

# Allow Vue Router to handle SPA paths (login/dashboard/etc)
@app.get("/{path:path}")
def spa_catch_all(path: str):
    return FileResponse(os.path.join(frontend_dist, "index.html"))

# ---------------- DATABASE SESSION ---------------- #

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ---------------- AUTH ---------------- #

@app.post('/token', response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    access_token_expires = timedelta(minutes=60*24)
    access_token = auth.create_access_token(
        data={'sub': user.username, 'role': user.role},
        expires_delta=access_token_expires
    )
    return {'access_token': access_token, 'token_type': 'bearer'}

# ---------------- USER & AUTH HELPERS ---------------- #

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    return user

@app.post('/users', response_model=dict)
def create_user(u: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, u.username, u.password, u.role)
    return {'username': user.username, 'role': user.role}

# ---------------- BOOKS / TRANSACTIONS ---------------- #

@app.get('/books')
def list_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

@app.post('/transactions', response_model=schemas.TransactionOut)
def add_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_transaction(db, tx, entered_by=current_user.username)

@app.get('/books/{book_name}/daily-summary')
def book_daily_summary(book_name: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    rows = crud.daily_summary(db, book_name)
    return [
        dict(date=r.date.isoformat(), item=r.item, department=r.department, total_qty=r.total_qty, total_value=r.total_value)
        for r in rows
    ]

# ---------------- SEED INITIAL DATA ---------------- #

@app.on_event('startup')
def seed_data():
    db = SessionLocal()
    try:
        if not crud.get_user_by_username(db, 'admin'):
            crud.create_user(db, 'admin', 'Admin', 'admin')
            print('Admin user created: admin / Admin')
        crud.create_book_if_not_exists(db, 'Injection Book')
        existing = db.query(models.Transaction).count()
        if existing == 0:
            tx = schemas.TransactionCreate(
                date=date.today(),
                item='Paracetamol Injection',
                quantity=5,
                rate=20,
                department='Ward 1',
                book_name='Injection Book'
            )
            crud.create_transaction(db, tx, entered_by='admin')
    finally:
        db.close()
