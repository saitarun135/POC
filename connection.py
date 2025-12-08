from database import SessionLocal
def connector():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()