from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter(tags=["identity"])

_NOT_IMPLEMENTED = JSONResponse({"message": "not implemented"}, status_code=501)


@router.post("/auth/register")
def register() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.post("/auth/login")
def login() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.post("/auth/refresh")
def refresh() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.post("/auth/logout")
def logout() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.get("/me")
def get_me() -> JSONResponse:
    return _NOT_IMPLEMENTED


@router.post("/me/pin")
def set_pin() -> JSONResponse:
    return _NOT_IMPLEMENTED
