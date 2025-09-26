from sqlalchemy.orm import Session
from . import models, schemas

def get_person(db: Session, person_id: int):
    return db.query(models.Person).filter(models.Person.id == person_id).first()

def get_persons(db: Session):
    return db.query(models.Person).all()

def create_person(db: Session, person: schemas.PersonRequest):
    db_person = models.Person(**person.dict())
    db.add(db_person)
    db.commit()
    db.refresh(db_person)
    return db_person

def update_person(db: Session, person_id: int, person: schemas.PersonRequest):
    db_person = get_person(db, person_id)
    if not db_person:
        return None
    for key, value in person.dict(exclude_unset=True).items():
        setattr(db_person, key, value)
    db.commit()
    db.refresh(db_person)
    return db_person

def delete_person(db: Session, person_id: int):
    db_person = get_person(db, person_id)
    if not db_person:
        return False
    db.delete(db_person)
    db.commit()
    return True