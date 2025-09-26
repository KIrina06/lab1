from fastapi import FastAPI, Depends, HTTPException, status, Response, Request, APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.orm import Session
from typing import List
from . import models, schemas, crud
from .database import SessionLocal, engine, Base

# Создаём таблицы
Base.metadata.create_all(bind=engine)

# FastAPI с префиксом для OpenAPI
app = FastAPI(
    title="Persons API",
    version="v1",
    openapi_url="/api/v1/openapi.json",
    docs_url="/api/v1/docs",
    redoc_url="/api/v1/redoc"
)

router = APIRouter(prefix="/api/v1")

# --- DB dependency ---
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Exception handlers на FastAPI (не на router!) ---
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = {}
    for err in exc.errors():
        loc = [str(p) for p in err.get("loc", []) if p != "body"]
        key = ".".join(loc) if loc else "body"
        errors.setdefault(key, []).append(err.get("msg"))
    errors = {k: "; ".join(v) for k, v in errors.items()}
    return JSONResponse(status_code=400, content={"message": "Invalid data", "errors": errors})

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(status_code=exc.status_code, content={"message": str(exc.detail)})

# --- Endpoints ---
@router.get("/persons/{id}", response_model=schemas.PersonResponse,
            responses={404: {"model": schemas.ErrorResponse}})
def read_person(id: int, db: Session = Depends(get_db)):
    p = crud.get_person(db, id)
    if not p:
        raise HTTPException(status_code=404, detail="Not found Person for ID")
    return p

@router.get("/persons", response_model=List[schemas.PersonResponse])
def read_persons(db: Session = Depends(get_db)):
    return crud.get_persons(db)

@router.post("/persons", status_code=201,
             responses={
                 201: {"description": "Created new Person",
                       "headers": {"Location": {"schema": {"type": "string"}}}},
                 400: {"model": schemas.ValidationErrorResponse}
             })
def create_person(person: schemas.PersonRequest, db: Session = Depends(get_db)):
    created = crud.create_person(db, person)
    return Response(status_code=201, headers={"Location": f"/api/v1/persons/{created.id}"})

@router.patch("/persons/{id}", response_model=schemas.PersonResponse,
              responses={400: {"model": schemas.ValidationErrorResponse},
                         404: {"model": schemas.ErrorResponse}})
def patch_person(id: int, person: schemas.PersonRequest, db: Session = Depends(get_db)):
    updated = crud.update_person(db, id, person)
    if not updated:
        raise HTTPException(status_code=404, detail="Not found Person for ID")
    return updated

@router.delete("/persons/{id}", status_code=204,
               responses={404: {"model": schemas.ErrorResponse}})
def delete_person(id: int, db: Session = Depends(get_db)):
    ok = crud.delete_person(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="Not found Person for ID")
    return Response(status_code=204)

# --- Подключаем router к приложению ---
app.include_router(router)