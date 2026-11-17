from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["funding"])

_NOT_IMPLEMENTED = JSONResponse({"message": "not implemented"}, status_code=501)


@router.post("/funding/topups")
def create_topup() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.post("/funding/withdrawals")
def create_withdrawal() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.get("/funding/{operation_id}")
def get_funding_operation(operation_id: str) -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.post("/webhooks/provider")
def provider_webhook() -> JSONResponse:
    return _NOT_IMPLEMENTED
