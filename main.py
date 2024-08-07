# from fastapi import FastAPI, Request, Form, Depends, File, UploadFile
# from fastapi.responses import HTMLResponse, RedirectResponse

# from fastapi_login import LoginManager
# from fastapi.security import OAuth2PasswordRequestForm
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi_login import LoginManager

import os, base64

import ZODB, ZODB.FileStorage
import transaction
import BTrees._OOBTree
import random
import string
from datetime import datetime, timedelta
import os

class NotAuthenticatedException(Exception):
    pass

def generate_session():
    return base64.b64encode(os.urandom(32))

SECRET = generate_session()

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
 
#home page
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})