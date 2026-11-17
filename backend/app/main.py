from fastapi import FastAPI

from app.modules.admin.router import router as admin_router
from app.modules.fees_limits.router import router as fees_limits_router
from app.modules.funding.router import router as funding_router
from app.modules.history.router import router as history_router
from app.modules.identity.router import router as identity_router
from app.modules.ledger.router import router as ledger_router
from app.modules.transfers.router import router as transfers_router
from app.modules.wallets.router import router as wallets_router

app = FastAPI(
    title="Vault API",
    description="Sandbox digital wallet with real banking logic",
    version="0.1.0",
)

app.include_router(identity_router, prefix="/api/v1")
app.include_router(wallets_router, prefix="/api/v1")
app.include_router(ledger_router, prefix="/api/v1")
app.include_router(transfers_router, prefix="/api/v1")
app.include_router(funding_router, prefix="/api/v1")
app.include_router(fees_limits_router, prefix="/api/v1")
app.include_router(history_router, prefix="/api/v1")
app.include_router(admin_router, prefix="/api/v1")


@app.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}
