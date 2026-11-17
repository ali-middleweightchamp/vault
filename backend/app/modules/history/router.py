from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["history"])

_NOT_IMPLEMENTED = JSONResponse({"message": "not implemented"}, status_code=501)


@router.get("/transactions")
def list_transactions() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.get("/transactions/{transaction_id}")
def get_transaction(transaction_id: str) -> JSONResponse:
    return _NOT_IMPLEMENTED
