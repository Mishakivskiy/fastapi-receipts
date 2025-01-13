from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.models import Receipt, ReceiptProduct, User
from app.schemas.receipt import ReceiptCreate, ReceiptItem, Product, Payment, ReceiptItemText


def create_receipt(db: Session, user_id: int, receipt_data: ReceiptCreate):
    total = 0
    products = []
    for product in receipt_data.products:
        product_total = product.price * product.quantity
        total += product_total
        products.append(ReceiptProduct(
            name=product.name,
            price=product.price,
            quantity=product.quantity,
            total=product_total
        ))

    if receipt_data.payment.amount < total:
        raise HTTPException(status_code=400, detail="Insufficient payment amount")

    rest = receipt_data.payment.amount - total

    receipt = Receipt(
        user_id=user_id,
        total=total,
        payment_type=receipt_data.payment.type,
        payment_amount=receipt_data.payment.amount,
        rest=rest,
        products=products
    )
    db.add(receipt)
    db.commit()
    db.refresh(receipt)
    return {"id": receipt.id,
            "products": receipt.products,
            "payment": {
                "type": receipt.payment_type,
                "amount": receipt.payment_amount
            },
            "total": total,
            "rest": rest,
            "created_at": receipt.created_at}


def get_receipts(db: Session, user_id: int, filters: dict = None, offset: int = 0, limit: int = 10):
    query = db.query(Receipt).filter(Receipt.user_id == user_id)

    if filters:
        if "date_from" in filters:
            query = query.filter(Receipt.created_at >= filters["date_from"])
        if "date_to" in filters:
            query = query.filter(Receipt.created_at <= filters["date_to"])
        if "payment_type" in filters:
            query = query.filter(Receipt.payment_type == filters["payment_type"])
        if "min_total" in filters:
            query = query.filter(Receipt.total >= filters["min_total"])
        if "max_total" in filters:
            query = query.filter(Receipt.total <= filters["max_total"])

    receipts = query.offset(offset).limit(limit).all()

    result = []
    for receipt in receipts:
        receipt_data = ReceiptItem(
            id=receipt.id,
            total=receipt.total,
            rest=receipt.rest,
            created_at=receipt.created_at,
            products=[Product(
                name=product.name,
                price=product.price,
                quantity=product.quantity,
                total=product.total
            ) for product in receipt.products],
            payment=Payment(
                type=receipt.payment_type,
                amount=receipt.payment_amount
            )
        )
        result.append(receipt_data)

    return result


def get_receipt_by_id(db: Session, receipt_id: int, user_id: int = None):
    query = db.query(Receipt).filter(Receipt.id == receipt_id)
    if user_id:
        query = query.filter(Receipt.user_id == user_id)

    receipt = query.first()
    if not receipt:
        return None

    receipt_item = ReceiptItemText(
        id=receipt.id,
        user_id=receipt.user_id,
        total=receipt.total,
        rest=receipt.rest,
        created_at=receipt.created_at,
        products=[Product(
            name=product.name,
            price=product.price,
            quantity=product.quantity,
            total=product.total
        ) for product in receipt.products],
        payment=Payment(
            type=receipt.payment_type,
            amount=receipt.payment_amount
        )
    )

    return receipt_item


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def generate_receipt_text(receipt: Receipt, user_name: str, line_width: int = 32):
    lines = [f"{user_name:^{line_width}}", "=" * line_width]

    for product in receipt.products:
        product_line = f"{product.quantity:.2f} x {product.price:,.2f} {product.total:,.2f}"
        name_line = f"{product.name[:line_width - 10]:<{line_width - 10}} {product.price:,.2f}"

        lines.append(product_line)
        lines.append(name_line)

    lines.append("=" * line_width)
    lines.append(f"СУМА {receipt.total:,.2f}".rjust(line_width))
    lines.append(f"{receipt.payment.type.capitalize()} {receipt.payment.amount:,.2f}".rjust(line_width))
    lines.append(f"Решта {receipt.rest:,.2f}".rjust(line_width))
    lines.append("=" * line_width)
    lines.append(f"{receipt.created_at:%d.%m.%Y %H:%M}".center(line_width))
    lines.append(f"{'Дякуємо за покупку!':^{line_width}}")

    return "<pre>\n" + "\n".join(lines) + "\n</pre>"
