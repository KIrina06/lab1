from pydantic import BaseModel
from typing import Optional, Dict

class PersonRequest(BaseModel):
    name: str
    age: Optional[int] = None
    address: Optional[str] = None
    work: Optional[str] = None

class PersonResponse(PersonRequest):
    id: int
    class Config:
        orm_mode = True

class ValidationErrorResponse(BaseModel):
    message: str
    errors: Dict[str, str]

class ErrorResponse(BaseModel):
    message: str