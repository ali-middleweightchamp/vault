from fastapi import APIRouter

router = APIRouter(tags=["ledger"])
# No public HTTP endpoints — ledger is accessed only via its service layer
