from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI(title="Vault Provider Simulator", version="0.1.0")

# Test cards (not real card numbers — simulator only):
#   4242 4242 4242 4242  — success after short delay
#   4000 0000 0000 0002  — decline: insufficient funds
#   4000 0000 0000 0119  — success with long delay (tests status polling)
#   4000 0000 0000 0341  — success + duplicate webhook (tests idempotency)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "provider-sim"}


@app.post("/v1/charges")
def create_charge() -> JSONResponse:
    return JSONResponse({"message": "not implemented"}, status_code=501)


@app.post("/v1/payouts")
def create_payout() -> JSONResponse:
    return JSONResponse({"message": "not implemented"}, status_code=501)


@app.get("/v1/operations/{operation_id}")
def get_operation(operation_id: str) -> JSONResponse:
    return JSONResponse({"message": "not implemented"}, status_code=501)
