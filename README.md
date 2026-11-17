```
██╗   ██╗ █████╗ ██╗   ██╗██╗  ████████╗
██║   ██║██╔══██╗██║   ██║██║  ╚══██╔══╝
██║   ██║███████║██║   ██║██║     ██║
╚██╗ ██╔╝██╔══██║██║   ██║██║     ██║
 ╚████╔╝ ██║  ██║╚██████╔╝███████╗██║
  ╚═══╝  ╚═╝  ╚═╝ ╚═════╝ ╚══════╝╚═╝
```

> **⚠ Demo: virtual money only. No real funds, no real payments.**

**Vault** is a sandbox digital wallet with real banking logic — built as a portfolio project to demonstrate how money actually moves in production financial systems.

![Stage](https://img.shields.io/badge/stage-0%20scaffold-orange)
![Python](https://img.shields.io/badge/python-3.12-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688)
![React](https://img.shields.io/badge/React-18-61DAFB)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What makes this interesting

Most "wallet" tutorials are CRUD apps with a `balance` column. Vault is not.

### Double-entry ledger
Every satoshi is accounted for. Money doesn't change — it *moves*. A transfer between two users creates three ledger entries that sum to zero:

```
wallet_A   -101 000 UZS   (sender pays amount + fee)
wallet_B   +100 000 UZS   (recipient receives)
fees         +1 000 UZS   (system collects fee)
─────────────────────────
Σ =              0        ✓ always
```

No balance column is ever mutated directly. Balance = sum of all entries for that account. This makes double-spending and "lost money" impossible by construction.

### Idempotency
Every money-moving `POST` requires an `Idempotency-Key` header (UUID). The same key returns the same response — no double charges if the network blips. Webhook delivery from the payment simulator is idempotent too.

### Concurrency
100 parallel transfers from the same wallet won't produce a negative balance. Accounts are locked in a deterministic order (`SELECT ... FOR UPDATE`) inside a single ACID transaction. No application-level locks, no optimistic retry loops.

### Outbox pattern
Events (notifications, fraud signals) are written in the same DB transaction as the transfer itself. A background worker publishes them reliably — no event is lost even if the process crashes mid-flight.

---

## Tech stack

| Layer | Technology |
|---|---|
| API | Python 3.12, FastAPI, Pydantic v2 |
| ORM / Migrations | SQLAlchemy 2.0 (sync), Alembic |
| Database | PostgreSQL 16 |
| Cache / Queues | Redis 7 |
| Auth | JWT (access + refresh), Argon2 PIN hashes |
| Background jobs | ARQ or Celery (ADR pending) |
| Frontend | React 18, Vite, TypeScript |
| State / Data | Zustand, TanStack Query |
| UI | Tailwind CSS, shadcn/ui, Recharts |
| Tests | pytest, Hypothesis (property-based), Testcontainers |
| CI | GitHub Actions, ruff, mypy, import-linter |
| Infra | Docker Compose, Caddy (production TLS) |

---

## Quick start

```bash
git clone https://github.com/your-org/vault
cd vault
cp .env.example .env
docker compose up
```

| Service | URL |
|---|---|
| API + Swagger | http://localhost:8000/docs |
| Frontend | http://localhost:3000 |
| Provider Simulator | http://localhost:8001/docs |

---

## Project structure

```
vault/
├── backend/                  # FastAPI modular monolith
│   ├── app/
│   │   ├── modules/
│   │   │   ├── identity/     # auth, JWT, sessions, PIN
│   │   │   ├── wallets/      # wallet CRUD, freeze/unfreeze
│   │   │   ├── ledger/       # double-entry core (append-only)
│   │   │   ├── transfers/    # P2P transfers with idempotency
│   │   │   ├── funding/      # top-ups, withdrawals, webhooks
│   │   │   ├── fees_limits/  # fee rules and limit rules
│   │   │   ├── history/      # transaction history, cursor pagination
│   │   │   ├── admin/        # admin tools, audit log
│   │   │   └── risk/         # fraud signals (Phase 3)
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── main.py
│   │   └── worker.py         # background process entry point
│   ├── alembic/              # DB migrations
│   ├── tests/
│   └── pyproject.toml
├── frontend/                 # React SPA (wallet + admin UI)
│   └── src/
├── provider-sim/             # Fake payment provider (webhooks, test cards)
├── docs/
│   └── adr/                  # Architecture Decision Records
├── .github/workflows/        # CI: lint, types, tests
├── docker-compose.yml
└── .env.example
```

Each module has the same shape: `router` → `service` → `repository` → `models`. Modules communicate **only** through each other's public `service` functions — `import-linter` enforces this in CI.

---

## Test cards (provider simulator)

| Card number | Behavior |
|---|---|
| `4242 4242 4242 4242` | Success after a short delay |
| `4000 0000 0000 0002` | Decline: insufficient funds |
| `4000 0000 0000 0119` | Success with long delay (tests status polling) |
| `4000 0000 0000 0341` | Success + duplicate webhook (tests idempotency) |

---

## Roadmap

```
Stage 0 ✅  Scaffold — repo, Docker Compose, CI, empty modules with interfaces
Stage 1 🔲  Core — ledger (double-entry), wallets, identity (JWT, PIN)
Stage 2 🔲  Money moves — P2P transfers, top-up/withdrawal, provider simulator, outbox worker
Stage 3 🔲  Polish — fees/limits, history, admin panel, full React UI, deploy to VPS
─── future ──────────────────────────────────────────────────────────────────
Phase 2     USD wallet, FX conversion, 2FA, KYC levels, PDF/CSV statements
Phase 3     Reconciliation, audit role, anti-fraud rules
Phase 4     Flutter mobile app
```

---

## Architecture decisions

Non-obvious choices are recorded in [`docs/adr/`](docs/adr/). Open decisions (sync vs async SQLAlchemy, ARQ vs Celery, locking strategy, etc.) live there as proposals until the team resolves them.

---

## Contributing

This is a learning project. PRs to `ledger` and `transfers` require review from both core contributors. Tests for money-handling code come before implementation.

---

<sub>Vault is a sandbox. It is not a bank, does not hold real money, and does not require a financial license. All amounts are virtual.</sub>
