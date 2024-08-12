import base64
from datetime import datetime
from fastapi import APIRouter, Depends, Request
from app.api.dependencies import *
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from app.db import models, schema, crud
from sqlalchemy.orm import Session

transferMoney = APIRouter()

transferMoney.mount("/static", StaticFiles(directory="app/static"), name="static")


@transferMoney.get("/transfer", response_class=HTMLResponse)
async def transfer(request: Request, db: Session = Depends(get_db), user=Depends(manager)):
    if isinstance(user, models.UserAccount):
        accounts = crud.getBankAccountsOfUser(db, user.id)
        return templates.TemplateResponse("transfer.html", {"request": request, "firstname": user.firstname,  "accounts": accounts})
    return RedirectResponse(url="/admin-home", status_code=302)

@transferMoney.post("/transferReview")
async def transferReview(request: schema.TransferReviewRequest, db: Session = Depends(get_db), user=Depends(manager)):
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    transferSchema = schema.TransferCreate(
        banknumber = request.banknumber,
        transferBankId = request.transferBankId,
        amount = request.amount,
        fee = 0.0,
        date = date,
        time = time,
        transferType = "Withdraw",
        receiver = request.banknumberReceiver
    )
    
    transfer = crud.createTransfer(db, transferSchema)
    
    return JSONResponse(
        status_code=201,
        content={"transferId": transfer.id}
    )

@transferMoney.get("/transferReview/{transferId}", response_class=HTMLResponse)
async def transferReview(request: Request, transferId: str, user=Depends(manager), db: Session = Depends(get_db)):
    if isinstance(user, models.UserAccount):
        decodetransferID = (base64.b64decode(transferId.encode('utf-8'))).decode('utf-8')
        transferID = int(decodetransferID.split("=")[1])
        transfer = crud.getTransfer(db, transferID)
        if transfer is None:
            return RedirectResponse(url="/transfer", status_code=302)
        bankAccount = crud.getBankAccount(db, transfer.bankAccount_id)
        newBalance = float(bankAccount.balance) - float(transfer.amount)
        return templates.TemplateResponse("transferReview.html", {"request": request, "firstname": user.firstname, "banknumber": bankAccount.banknumber, "balance": newBalance, "amount": transfer.amount, "fee": transfer.fee, "transferBankId": transfer.transferBankId, "banknumberReceiver": transfer.receiver, "totalAmount": transfer.amount})
    return RedirectResponse(url="/admin-home", status_code=302)
    
@transferMoney.post("/confirmTransfer")
async def confirmTransfer(request: schema.TransferRequest, user=Depends(manager), db: Session = Depends(get_db)):
    transfer = crud.getTransfer(db, request.transactionId)
    bankNumber = transfer.bankAccount_id
    updated = crud.updateBalanceTransfer(db, bankNumber, transfer.amount, transfer.receiver, transfer.transferBankId)
    if updated == False:
        return JSONResponse(
            status_code=400,
            content={"detail": "Invalid receiver account"}
        )
        
    return JSONResponse(
        status_code=201,
        content={"detail": "Transaction successful"}
    )

@transferMoney.delete("/removeTransfer")
async def deleteTransfer(request: schema.TransferRequest, db: Session = Depends(get_db)):
    crud.deleteTransfer(db, request.transactionId)
    return JSONResponse(
        status_code=200,
        content={"detail": "Transaction deleted"}
    )