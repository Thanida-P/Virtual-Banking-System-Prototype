from fastapi import APIRouter, Depends, Request
from app.api.dependencies import *
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from app.db import models, schema, crud
from sqlalchemy.orm import Session

transactionMoney = APIRouter()

transactionMoney.mount("/static", StaticFiles(directory="app/static"), name="static")

#transaction
@transactionMoney.get("/transaction", response_class=HTMLResponse)
async def transaction(request: Request, user=Depends(manager), db: Session = Depends(get_db)):
    if isinstance(user, models.UserAccount):
        accounts = crud.getBankAccountsOfUser(db, user.id)
        return templates.TemplateResponse("transaction.html", {"request": request, "firstname": user.firstname,  "accounts": accounts})
    return RedirectResponse(url="/admin-home", status_code=302)

@transactionMoney.post("/transaction")
async def transaction(request: schema.TransactionRequest, user=Depends(manager), db: Session = Depends(get_db)):
    if isinstance(user, models.UserAccount):
        action = request.action
        phone = request.phno
        amount = request.amount
        banknumber = request.banknumber
        
        bankAccount = crud.getBankAccount(db, banknumber)
        
        if phone == user.phone and bankAccount.accountId == user.id:
            updated = crud.updateBalanceTransaction(db, banknumber=banknumber, amount=amount, action=action)
            if updated == False:
                return JSONResponse(
                    status_code=400,
                    content={"detail": "Invalid account number"}
                )
            return JSONResponse(
                status_code=201,
                content={"detail": "Transaction successful"}
            )
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid phone number or account number"}
        )