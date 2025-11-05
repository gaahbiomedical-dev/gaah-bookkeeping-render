from sqlalchemy.orm import Session
from . import models, schemas, auth
from sqlalchemy import func
def create_user(db: Session, username: str, password: str, role: str = 'user'):
    hashed = auth.get_password_hash(password)
    user = models.User(username=username, hashed_password=hashed, role=role)
    db.add(user); db.commit(); db.refresh(user)
    return user
def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()
def create_book_if_not_exists(db: Session, name: str):
    book = db.query(models.Book).filter(models.Book.name == name).first()
    if not book:
        book = models.Book(name=name)
        db.add(book); db.commit(); db.refresh(book)
    return book
def create_transaction(db: Session, tx: schemas.TransactionCreate, entered_by: str):
    book = create_book_if_not_exists(db, tx.book_name or 'Default')
    total = tx.total if tx.total else (tx.quantity * tx.rate)
    db_tx = models.Transaction(
        date=tx.date,
        item=tx.item,
        quantity=tx.quantity,
        rate=tx.rate,
        total=total,
        patient=tx.patient,
        department=tx.department,
        book_id=book.id,
        entered_by=entered_by
    )
    db.add(db_tx); db.commit(); db.refresh(db_tx)
    return db_tx
def daily_summary(db: Session, book_name: str):
    book = db.query(models.Book).filter(models.Book.name == book_name).first()
    if not book:
        return []
    q = (
        db.query(models.Transaction.date, models.Transaction.item, models.Transaction.department,
                 func.sum(models.Transaction.quantity).label('total_qty'),
                 func.sum(models.Transaction.total).label('total_value'))
        .filter(models.Transaction.book_id == book.id)
        .group_by(models.Transaction.date, models.Transaction.item, models.Transaction.department)
        .order_by(models.Transaction.date.desc())
    )
    return q.all()
