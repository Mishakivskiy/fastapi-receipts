from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
from sqlalchemy.orm import Session
from app.services.receipt_service import (create_receipt,
                                          get_receipts,
                                          get_receipt_by_id,
                                          generate_receipt_text,
                                          get_user_by_id)
from app.schemas.receipt import ReceiptCreate, ReceiptItem
from core.database import get_db
from app.services.auth import get_current_user


receipt_router = APIRouter()


@receipt_router.post("/", response_model=ReceiptItem)
def create_new_receipt(receipt_data: ReceiptCreate, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    return create_receipt(db, user.id, receipt_data)


@receipt_router.get("/")
def list_receipts(
        db: Session = Depends(get_db),
        user: dict = Depends(get_current_user),
        offset: int = 0,
        limit: int = 10,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        payment_type: Optional[str] = None,
        min_total: Optional[float] = None,
        max_total: Optional[float] = None
):
    filters = {
        "date_from": date_from,
        "date_to": date_to,
        "payment_type": payment_type,
        "min_total": min_total,
        "max_total": max_total,
    }

    filters = {key: value for key, value in filters.items() if value is not None}

    return get_receipts(db, user.id, filters=filters, offset=offset, limit=limit)


@receipt_router.get("/{receipt_id}", response_model=ReceiptItem)
def get_receipt(receipt_id: int, db: Session = Depends(get_db), user: dict = Depends(get_current_user)):
    receipt_item = get_receipt_by_id(db, receipt_id, user.id)
    if not receipt_item:
        raise HTTPException(status_code=404, detail="Receipt not found")
    return receipt_item


@receipt_router.get("/{receipt_id}/text", response_class=HTMLResponse)
def generate_receipt_text_endpoint(receipt_id: int, db: Session = Depends(get_db)):
    receipt = get_receipt_by_id(db, receipt_id)

    if not receipt:
        raise HTTPException(status_code=404, detail="Receipt not found")

    print(receipt)

    user = get_user_by_id(db, receipt.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    receipt_text = generate_receipt_text(receipt, user_name=user.name)

    return receipt_text
