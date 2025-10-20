from pydantic import BaseModel, EmailStr, Field

# What we send back to clients
class UserOut(BaseModel):
    id: int
    full_name: str
    email: EmailStr
    
    class Config:
        from_attributes = True # allow ORM (SQLAlchemy) -> Pydantic conversion

# What a client sends to create a user
class UserCreate(BaseModel):
    full_name: str = Field(min_length=1, max_length=120)
    email: EmailStr
    
# Partial update
class UserUpdate (BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=120)
    email: EmailStr | None = None
