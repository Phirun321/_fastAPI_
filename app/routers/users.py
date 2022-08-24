
from fastapi import APIRouter, Form
from fastapi import Body,status,APIRouter,HTTPException
from typing import List
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from database.connection.mongodb import mongodb
from database.models.users import StudentModel,UpdateStudentModel,Token
from passlib.context import CryptContext
from utils.functions import authenticate_user
from utils.jwt import signJWT
from utils.auth_bearer import verify_isAdmin, current_user, access_token
from fastapi import HTTPException, Depends
# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
db = mongodb()
router = APIRouter()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
collection_name = 'students'
userModel = StudentModel
userUpdateModel = UpdateStudentModel


### function encrypt password
def get_password_hash(password):
    return pwd_context.hash(password)


#### create user ####
@router.post("/api/create_users/", tags=["users"],
response_description="Add new student", 
response_model=StudentModel,
# dependencies=[Depends(oauth2_scheme)])
)
async def create_student(student: StudentModel = Body(...)):
    student = jsonable_encoder(student)
    user_existing = await db[collection_name].find_one({"email":student['email']})
    if user_existing == None:
      password = student['password']
      bcrype_password = get_password_hash(password)
      student['password'] = bcrype_password
      new_student = await db["students"].insert_one(student)
      created_student = await db["students"].find_one({"_id": new_student.inserted_id})
      return JSONResponse(
          status_code=status.HTTP_201_CREATED, 
          content={
              "data":created_student,
              "message":'create success',
              "statusCode":201
              }
          )
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email already exist"
        )

#### get all users ####
@router.get(
    "/api/users/", 
    response_description="List all students", 
    response_model=List[StudentModel], 
    tags=["users"], 
    dependencies=[Depends(verify_isAdmin)]
    )
async def list_students():
    students = await db[collection_name].find().to_list(1)
    return students
 
#### get users via specific id ####
@router.get("/api/user/{id}", response_description="Get a single student", 
response_model=StudentModel, tags=["users"])
async def show_student(id: str):
    if (student := await db[collection_name].find_one({"_id": id})) is not None:
        return student
        
    raise HTTPException(status_code=404, detail=f"Student {id} not found")
 
#### update users ####
@router.put("/api/user/{id}", response_description="Update a student", response_model=StudentModel, tags=["users"])
async def update_student(id: str, student: UpdateStudentModel = Body(...)):
    student = {k: v for k, v in student.dict().items() if v is not None}

    if len(student) >= 1:
        update_result = await db[collection_name].update_one({"_id": id}, {"$set": student})

        if update_result.modified_count == 1:
            if (
                updated_student := await db[collection_name].find_one({"_id": id})
            ) is not None:
                return updated_student

    if (existing_student := await db[collection_name].find_one({"_id": id})) is not None:
        return existing_student

    raise HTTPException(status_code=404, detail=f"Student {id} not found")

#### delete user ####
@router.delete("/api/user/{id}" , response_description="Delete a student",tags=["users"])
async def delete_student(id: str):
    delete_result = await db[collection_name].delete_one({"_id": id})
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)
    raise HTTPException(status_code=404, detail=f"Student {id} not found")

#### user login ####    
@router.post("/api/login",
response_description="User login to get token", 
response_model=Token, tags=["users"])
async def userLogin (email:str = Form(...), password: str = Form(...)):
    #find all data in students collection
    students = [doc async for doc in db[collection_name].find()]
    user = await authenticate_user(students, email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    token = signJWT(user)
    return {"access_token": token['access_token'], "token_type": "bearer"}