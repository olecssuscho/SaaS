from pydantic import BaseModel, EmailStr, field_validator, Field

class UserMODELS(BaseModel):
    email : EmailStr 
    password : str = Field(examples=["MyPass#2024"])
    fullname : str

    @field_validator("password")
    @classmethod
    def validate_password(cls,v : str) -> str:
        if len(v)<8:
            return ValueError("Password must be at least 8 characters")
        if not any(c.isdigit() for c in v):
            return ValueError("Password must be at least 8 characters")
        if not any(c.isupper() for c in v):
            return ValueError("Password must be at least 8 characters")
        if not any(c in "!@#$%^&*" for c in v):
            raise ValueError("Password must contain a special character")
        return v


