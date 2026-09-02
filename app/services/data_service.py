from typing import List, Optional

import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.record import SalesRecord
from app.schemas.record import SalesRecordCreate


def create_record(db: Session, record: SalesRecordCreate) -> SalesRecord:
    try:
        db_record = SalesRecord(**record.model_dump())
        db.add(db_record)
        db.commit()
        db.refresh(db_record)
        return db_record
    except SQLAlchemyError:
        db.rollback()
        raise


def create_records_batch(
    db: Session,
    records: List[SalesRecordCreate]
) -> List[SalesRecord]:
    data = [record.model_dump() for record in records]

    df = pd.DataFrame(data)

    string_columns = [
        "product_name",
        "category",
        "customer_name",
        "region",
    ]

    for column in string_columns:
        df[column] = df[column].astype(str).str.strip()

    if df[string_columns].eq("").any().any():
        raise ValueError("Text fields cannot be empty after trimming")

    df["category"] = df["category"].str.title()
    df["region"] = df["region"].str.title()

    cleaned_records = [
        SalesRecord(**row)
        for row in df.to_dict(orient="records")
    ]

    try:
        db.add_all(cleaned_records)
        db.commit()

        for record in cleaned_records:
            db.refresh(record)

        return cleaned_records
    except SQLAlchemyError:
        db.rollback()
        raise


def get_records(
    db: Session,
    skip: int = 0,
    limit: int = 100
) -> List[SalesRecord]:
    return (
        db.query(SalesRecord)
        .order_by(SalesRecord.id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_record(
    db: Session,
    record_id: int
) -> Optional[SalesRecord]:
    return (
        db.query(SalesRecord)
        .filter(SalesRecord.id == record_id)
        .first()
    )


def get_sales_summary(db: Session) -> dict:
    records = db.query(SalesRecord).all()

    if not records:
        return {
            "total_records": 0,
            "total_quantity": 0,
            "total_revenue": 0.0,
            "average_order_value": 0.0,
            "revenue_by_category": {},
        }

    data = [
        {
            "category": record.category,
            "quantity": record.quantity,
            "unit_price": record.unit_price,
        }
        for record in records
    ]

    df = pd.DataFrame(data)

    df["total_amount"] = (
        df["quantity"] * df["unit_price"]
    )

    revenue_by_category = (
        df.groupby("category")["total_amount"]
        .sum()
        .round(2)
        .to_dict()
    )

    return {
        "total_records": int(len(df)),
        "total_quantity": int(df["quantity"].sum()),
        "total_revenue": round(
            float(df["total_amount"].sum()),
            2,
        ),
        "average_order_value": round(
            float(df["total_amount"].mean()),
            2,
        ),
        "revenue_by_category": revenue_by_category,
    }
