from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.record import SalesRecordCreate, SalesRecordResponse
from app.services.data_service import (
    create_record,
    create_records_batch,
    get_record,
    get_records,
    get_sales_summary,
)

router = APIRouter()


@router.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "python-data-api"
    }


@router.post(
    "/records",
    response_model=SalesRecordResponse,
    status_code=status.HTTP_201_CREATED
)
def create_sales_record(
    record: SalesRecordCreate,
    db: Session = Depends(get_db)
):
    try:
        return create_record(db, record)
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create sales record"
        )


@router.post(
    "/records/batch",
    response_model=List[SalesRecordResponse],
    status_code=status.HTTP_201_CREATED
)
def create_sales_records_batch(
    records: List[SalesRecordCreate],
    db: Session = Depends(get_db)
):
    if not records:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one sales record is required"
        )

    try:
        return create_records_batch(db, records)
    except ValueError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc)
        )
    except SQLAlchemyError:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Unable to create sales records"
        )


@router.get(
    "/records",
    response_model=List[SalesRecordResponse]
)
def list_sales_records(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    db: Session = Depends(get_db)
):
    return get_records(db, skip=skip, limit=limit)


@router.get(
    "/records/{record_id}",
    response_model=SalesRecordResponse
)
def retrieve_sales_record(
    record_id: int,
    db: Session = Depends(get_db)
):
    record = get_record(db, record_id)

    if record is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sales record with id {record_id} not found"
        )

    return record


@router.get("/analytics/summary")
def sales_summary(db: Session = Depends(get_db)):
    return get_sales_summary(db)
