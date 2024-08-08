# from fastapi import FastAPI, Request, Form, Depends, File, UploadFile
# from fastapi.responses import HTMLResponse, RedirectResponse

# from fastapi_login import LoginManager
from object import *
import logging

logging.basicConfig(level=logging.INFO)

from fastapi import FastAPI, Request
from fastapi import FastAPI, Request, Form, Depends, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi_login import LoginManager
from fastapi.security import OAuth2PasswordRequestForm

import os, base64

from fastapi.security import OAuth2PasswordRequestForm
import ZODB, ZODB.FileStorage
import transaction
import BTrees._OOBTree
from datetime import datetime, timedelta
import os

class NotAuthenticatedException(Exception):
    pass

def generate_session():
    return base64.b64encode(os.urandom(16))

SECRET = generate_session()

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

manager = LoginManager(SECRET, token_url='/login', use_cookie=True)
manager.cookie_name = "session"

storage = ZODB.FileStorage.FileStorage('data/bankData.fs')
db = ZODB.DB(storage)
connection = db.open()
root = connection.root

# #create root if it does not exist
if not hasattr(root, "customers"):
    root.customers = BTrees.OOBTree.BTree()
if not hasattr(root, "admin"):
    root.admin = BTrees.OOBTree.BTree()
if not hasattr(root, "accounts"):
    root.accounts = BTrees.OOBTree.BTree()
if not hasattr(root, "transfers"):
    root.transfers = BTrees.OOBTree.BTree()
if not hasattr(root, "withdrawals"):
    root.withdrawals = BTrees.OOBTree.BTree()
if not hasattr(root, "currency"):
    root.currency = BTrees.OOBTree.BTree()
    currencyID = ["USD", "EUR", "GBP", "JPY", "AUD", "CAD", "CHF", "CNY", "SGD", "HKD", "NZD", "SEK", "DKK", "NOK", "KRW", "TWD", "MYR", "IDR", "INR", "PHP", "VND", "ZAR"]
    currencyName = ["United States Dollar", "Euro", "British Pound Sterling", "Japanese Yen", "Australian Dollar", "Canadian Dollar", "Swiss Franc", "Chinese Yuan", "Singapore Dollar", "Hong Kong Dollar", "New Zealand Dollar", "Swedish Krona", "Danish Krone", "Norwegian Krone", "South Korean Won", "New Taiwan Dollar", "Malaysian Ringgit", "Indonesian Rupiah", "Indian Rupee", "Philippine Peso", "Vietnamese Dong", "South African Rand"]
    currencyRate = [
        [35.41, 35.57],  # USD
        [39.00, 39.17],  # EUR
        [45.10, 45.25],  # GBP
        [0.244, 0.246],  # JPY
        [23.94, 24.15],  # AUD
        [26.50, 26.70],  # CAD
        [40.12, 40.32],  # CHF
        [4.88, 4.91],    # CNY
        [26.83, 27.00],  # SGD
        [4.54, 4.57],    # HKD
        [21.10, 21.20],  # NZD
        [3.35, 3.37],    # SEK
        [5.23, 5.25],    # DKK
        [3.26, 3.28],    # NOK
        [0.025, 0.026],  # KRW
        [1.08, 1.10],    # TWD
        [7.95, 8.00],    # MYR
        [0.002, 0.0022], # IDR
        [0.423, 0.425],  # INR
        [0.615, 0.617],  # PHP
        [0.0015, 0.0016],# VND
        [1.92, 1.95]     # ZAR
    ]

    
    for i in range(len(currencyID)):
        root.currency[currencyID[i]] = Currency(currencyID[i], currencyName[i], currencyRate[i])
        transaction.commit()

if not hasattr(root, 'exchange_rates'):
    root.exchange_rates = BTrees.OOBTree.BTree()

if hasattr(root, 'exchange_rates'):
    for rate_id, rate in root.exchange_rates.items():
        print(f"Rate ID: {rate_id}")
        print(f"From: {rate.from_currency}")
        print(f"To: {rate.to_currency}")
        print(f"Sell Rate: {rate.sell_rate}")
        print(f"Buy Rate: {rate.buy_rate}")
else:
    print("No exchange rates found.")
  
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
    return templates.TemplateResponse("transfer.html", {"request": request})

#home
@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

@app.get("/transfer", response_class=HTMLResponse)
async def transfer(request: Request):
    return templates.TemplateResponse("transfer.html", {"request": request})

@app.get("/withdraw", response_class=HTMLResponse)
async def withdraw(request: Request):
    return templates.TemplateResponse("withdrawal.html", {"request": request})

@app.get("/withdraw/review", response_class=HTMLResponse)
async def withdrawReview(request: Request):
    return templates.TemplateResponse("withdrawalReview.html", {"request": request})

@app.get("/transfer/review", response_class=HTMLResponse)
async def transferReview(request: Request):
    return templates.TemplateResponse("transferReview.html", {"request": request})
         
@app.get("/currency-exchange", response_class=HTMLResponse)
async def currencyExchange(request: Request):
    return templates.TemplateResponse("currencyExchange.html", {"request": request})

@app.post("/get-currency-rate/{currencyID}")
async def getCurrencyRate(request: Request, currencyID: str):
    currencyRate = root.currency[currencyID].getCurrencyRate()
    return {"buyRate": currencyRate[0], "sellRate": currencyRate[1]}

@app.get("/fakeAtm", response_class=HTMLResponse)
async def fakeAtm(request: Request):
    return templates.TemplateResponse("fakeAtm.html", {"request": request})


#Currency Exchange Rate For Admin

@app.post("/admin/currency-exchange")
async def addCurrencyExchangeRate(
    request: Request,
    from_currency: str = Form(...,alias="from"),
    to_currency: str = Form(...,alias = "to"),
    sell_rate :float = Form(...,alias="sellRate"),
    buy_rate: float = Form(...,alias="buyRate")
):
    rate = CurrencyExchangeRate(from_currency, to_currency,sell_rate, buy_rate)
    rate_id = f"{from_currency}_{to_currency}"
    root.exchange_rates[rate_id] = rate
    transaction.commit()
    logging.info(f"Added exchange rate: {rate_id} - {rate}")
    return JSONResponse({"message": "Exchange rate added successfully!"}, status_code = 201)


@app.post("/admin/currency-exchange")
async def add_or_update_currency_exchange_rate(
    request: Request,
    from_currency: str = Form(..., alias="from"),
    to_currency: str = Form(..., alias="to"),
    sell_rate: float = Form(..., alias="sellRate"),
    buy_rate: float = Form(..., alias="buyRate")
):
    rate_id = f"{from_currency}_{to_currency}"
    
   
    if rate_id in root.exchange_rates:
        
        existing_rate = root.exchange_rates[rate_id]
        existing_rate.sell_rate = sell_rate
        existing_rate.buy_rate = buy_rate
        message = f"Updated exchange rate: {rate_id}"
    else:
       
        rate = CurrencyExchangeRate(from_currency, to_currency, sell_rate, buy_rate)
        root.exchange_rates[rate_id] = rate
        message = f"Added new exchange rate: {rate_id}"
    
    transaction.commit()
    logging.info(message)
    return JSONResponse({"message": message}, status_code=201)



@app.get("/admin/exchange-rates",response_class=JSONResponse)
async def get_exchange_rates():
    rates = []
    for rate_id, rate in root.exchange_rates.items():
        rates.append({
            "from_currency": rate.from_currency,
            "to_currency": rate.to_currency,
            "sell_rate": rate.sell_rate,
            "buy_rate": rate.buy_rate
        })

    return rates


