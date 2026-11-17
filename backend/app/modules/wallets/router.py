from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["wallets"])

_NOT_IMPLEMENTED = JSONResponse({"message": "not implemented"}, status_code=501)


@router.get("/wallets")
def list_wallets() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.get("/wallets/{wallet_id}")
def get_wallet(wallet_id: str) -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.post("/wallets/{wallet_id}/freeze")
def freeze_wallet(wallet_id: str) -> JSONResponse:
    return _NOT_IMPLEMENTED
