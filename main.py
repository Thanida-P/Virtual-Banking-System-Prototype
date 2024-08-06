from fastapi import FastAPI, Request, Form, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm
import ZODB, ZODB.FileStorage
import transaction
import BTrees._OOBTree
import random
import string
from datetime import datetime, timedelta
import os

class NotAuthenticatedException(Exception):
    pass

SECRET = 'xxx'

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

manager = LoginManager(SECRET, token_url='/login', use_cookie=True, custom_exception=NotAuthenticatedException)
manager.cookie_name = "session"

# storage = ZODB.FileStorage.FileStorage('data/userData.fs')
# db = ZODB.DB(storage)
# connection = db.open()
# root = connection.root

# #create root if it does not exist
# if not hasattr(root, "students"):
#     root.students = BTrees.OOBTree.BTree()
# if not hasattr(root, "teachers"):
#     root.teachers = BTrees.OOBTree.BTree()
# if not hasattr(root, "teacherCourses"):
#     root.teacherCourses = BTrees.OOBTree.BTree()
# if not hasattr(root, "studentCourses"):
#     root.studentCourses = BTrees.OOBTree.BTree()
# if not hasattr(root, "announcements"):
#     root.announcements = BTrees.OOBTree.BTree()
# if not hasattr(root, "assignments"):
#     root.assignments = BTrees.OOBTree.BTree()
# if not hasattr(root, "studentAssignments"):
#     root.studentAssignments = BTrees.OOBTree.BTree()
# if not hasattr(root, "attendances"):
#     root.attendances = BTrees.OOBTree.BTree()
# if not hasattr(root, "studentAttendances"):
#     root.studentAttendances = BTrees.OOBTree.BTree()
  
  
#load user
# @manager.user_loader()
# def load_user(email: str):
#     user = None

#     for t in root.teachers:
#         if email == root.teachers[t].getEmail():
#             user = root.teachers[t]
    
#     for s in root.students:
#         if email == root.students[s].getEmail():
#             user = root.students[s]

#     return user

#check if the user is login
# @app.exception_handler(NotAuthenticatedException)
# def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
#     return RedirectResponse(url='/login')

#redirect to the correct home page (teacher or student)
# @app.get("/", response_class=HTMLResponse)
# async def redirect(request: Request, user_info=Depends(manager)):
#     if isinstance(user_info, Student):
#         return RedirectResponse(url="/home_student", status_code=302)
#     elif isinstance(user_info, Teacher):
#         return RedirectResponse(url="/home_teacher", status_code=302)
 
#login
@app.get("/", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("fakeATMSuccess.html", {"request": request})