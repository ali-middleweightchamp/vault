from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["admin"])

_NOT_IMPLEMENTED = JSONResponse({"message": "not implemented"}, status_code=501)


@router.get("/admin/users")
def list_users() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.get("/admin/users/{user_id}")
def get_user(user_id: str) -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.post("/admin/users/{user_id}/freeze")
def freeze_user(user_id: str) -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.post("/admin/wallets/{wallet_id}/unfreeze")
def unfreeze_wallet(wallet_id: str) -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.get("/admin/ledger/transactions")
def list_ledger_transactions() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.get("/admin/audit-log")
def get_audit_log() -> JSONResponse:
    return _NOT_IMPLEMENTED
