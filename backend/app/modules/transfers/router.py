from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["transfers"])

_NOT_IMPLEMENTED = JSONResponse({"message": "not implemented"}, status_code=501)


@router.post("/transfers")
def create_transfer() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.get("/transfers/{transfer_id}")
def get_transfer(transfer_id: str) -> JSONResponse:
    return _NOT_IMPLEMENTED
