from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from sqlalchemy.orm import Session
from . import models, schemas, crud, auth
from .database import SessionLocal, engine
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import timedelta, date
from jose import jwt, JWTError
import os

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# OAuth2PasswordBearer to retrieve token from request
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

# Serve static frontend if built
if os.path.isdir(os.path.join(os.path.dirname(__file__), 'static')):
    app.mount('/', StaticFiles(directory=os.path.join(os.path.dirname(__file__), 'static'), html=True), name='static')

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Endpoint to get token and login the user
@app.post('/token', response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Incorrect username or password')
    
    access_token_expires = timedelta(minutes=60*24)
    access_token = auth.create_access_token(data={'sub': user.username, 'role': user.role}, expires_delta=access_token_expires)
    return {'access_token': access_token, 'token_type': 'bearer'}

# Endpoint to create a user
@app.post('/users', response_model=dict)
def create_user(u: schemas.UserCreate, db: Session = Depends(get_db)):
    user = crud.create_user(db, u.username, u.password, u.role)
    return {'username': user.username, 'role': user.role}

# Dependency to get the current logged-in user from the token
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Could not validate credentials')
    
    try:
        payload = jwt.decode(token, auth.SECRET_KEY, algorithms=['HS256'])
        username: str = payload.get('sub')
        role: str = payload.get('role', 'user')
        
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = crud.get_user_by_username(db, username)
    if user is None:
        raise credentials_exception
    
    return user

# Endpoint to list all books
@app.get('/books')
def list_books(db: Session = Depends(get_db)):
    return db.query(models.Book).all()

# Endpoint to add a transaction
@app.post('/transactions', response_model=schemas.TransactionOut)
def add_transaction(tx: schemas.TransactionCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return crud.create_transaction(db, tx, entered_by=current_user.username)

# Endpoint to get daily summary for a specific book
@app.get('/books/{book_name}/daily-summary')
def book_daily_summary(book_name: str, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    rows = crud.daily_summary(db, book_name)
    return [dict(date=r.date.isoformat(), item=r.item, department=r.department, total_qty=r.total_qty, total_value=r.total_value) for r in rows]

# Function to seed initial data (e.g. create admin user and default book/transaction)
@app.on_event('startup')
def seed_data():
    db = SessionLocal()
    try:
        if not crud.get_user_by_username(db, 'admin'):
            crud.create_user(db, 'admin', 'Admin', 'admin')  # Default admin user with password 'Admin'
            print('Admin user created: admin / Admin')
        
        crud.create_book_if_not_exists(db, 'Injection Book')
        
        # Check if there are any existing transactions
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
