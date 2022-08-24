import enum
from re import S
from pydantic import BaseModel,Field,EmailStr
from bson import ObjectId
from typing import Optional, Union

class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")
        
class StudentModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    email: EmailStr = Field(...)
    password:str = Field(...)
    course: str = Field(...)
    gpa: float = Field(..., le=4.0)
    role:str = Field(description="It has only three type such us |user|,|super user| and |admin| ")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "password":"12345",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
                "role":"admin"
            }
        }
        
class UpdateStudentModel(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr]
    password:Optional[str]
    course: Optional[str]
    gpa: Optional[float]
    role:Optional[str]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        env_file = ".env"
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jdoe@example.com",
                "password":"12345",
                "course": "Experiments, Science, and Fashion in Nanophotonics",
                "gpa": "3.0",
            }
        }
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None
    email:Union[str, None] = None

class User(BaseModel):
    username: str
    email: Union[str, None] = None
    full_name: Union[str, None] = None
    disabled: Union[bool, None] = None

class userLogin(BaseModel):
    email: Union[str, None] = None
    password: Union[str, None] = None