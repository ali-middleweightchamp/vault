from fastapi import APIRouter

router = APIRouter(tags=["fees_limits"])
# No public endpoints in Stage 0 — rules are read internally by transfers/funding
