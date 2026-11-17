# Vault — Project Roadmap

> Sandbox digital wallet with real banking logic. Built as a portfolio project to demonstrate double-entry bookkeeping, idempotency, concurrency, and ACID transactions.

---

## Stage 0 — Scaffold ✅
**Goal:** Working skeleton. `docker compose up` brings everything up. CI is green. Modules are empty but wired.

**Deliverables:**
- [x] Repository structure: `backend/`, `frontend/`, `provider-sim/`, `docs/`
- [x] Docker Compose: `db`, `redis`, `api`, `worker`, `provider-sim`, `web`
- [x] 9 backend modules with stubs (`identity`, `wallets`, `ledger`, `transfers`, `funding`, `fees_limits`, `history`, `admin`, `risk`)
- [x] CI pipeline: `ruff`, `mypy`, `import-linter`, `pytest`, `tsc`
- [x] Alembic setup
- [x] Skeleton OpenAPI (all endpoints return 501)
- [x] ADR folder

**Acceptance:** `GET /health` returns 200. CI is green.

---

## Stage 1 — Access & Core
**Goal:** A user can register, log in, and see their UZS wallet. The ledger engine works and is tested.

### 1a — Ledger Engine
The foundation. Everything else depends on this.

**Deliverables:**
- [ ] DB tables: `ledger_accounts`, `ledger_transactions`, `ledger_entries`
- [ ] Alembic migration: ledger tables
- [ ] `ledger.service.create_transaction(entries)` — atomic, validates zero-sum
- [ ] Balance calculation: `SELECT SUM(amount) FROM ledger_entries WHERE account_id = ?`
- [ ] Reversal: creates mirror entries with `reversal_of` reference
- [ ] **Property-based tests (Hypothesis):**
  - Sum of entries in any transaction = 0
  - Balance of account = sum of its entries
  - User account balance never goes negative
- [ ] Integration tests with real PostgreSQL (Testcontainers)

### 1b — Identity
**Deliverables:**
- [ ] DB tables: `users`, `user_sessions`
- [ ] Alembic migration: identity tables
- [ ] `POST /auth/register` — email, password, username
- [ ] Email verification flow (token sent, `GET /auth/verify-email?token=`)
- [ ] `POST /auth/login` — returns access + refresh JWT
- [ ] `POST /auth/refresh` — rotates refresh token
- [ ] `POST /auth/logout` — revokes session
- [ ] `GET /me/sessions`, `DELETE /me/sessions` (logout all)
- [ ] Password hashing: argon2
- [ ] JWT: access token (15 min), refresh token (30 days, hash stored in `user_sessions`)

### 1c — Wallets
**Deliverables:**
- [ ] DB table: `wallets`
- [ ] Auto-create UZS wallet on registration
- [ ] `GET /wallets` — list user's wallets
- [ ] `GET /wallets/{id}` — wallet details + balance (computed from ledger)
- [ ] `POST /wallets/{id}/freeze` — user self-freeze

### 1d — PIN
**Deliverables:**
- [ ] `POST /me/pin` — set PIN (hashed with argon2)
- [ ] PIN verification function (used by transfers in Stage 2)
- [ ] Failed attempt counter + temporary lockout (`pin_failed_attempts`, `pin_locked_until`)

**Stage 1 Acceptance:**
- User registers → email verified → sees UZS wallet with 0 balance
- Refresh token rotation works
- Property-based test on zero-sum is green
- Testcontainers integration tests pass in CI

---

## Stage 2 — Money Moves
**Goal:** Top up, transfer, withdraw. 100 concurrent transfers don't go negative. Duplicate webhook is ignored.

### 2a — Transfers (P2P)
**Deliverables:**
- [ ] DB table: `transfers`, `idempotency_keys`
- [ ] `POST /transfers` — P2P transfer by username
- [ ] PIN confirmation
- [ ] Idempotency: same `Idempotency-Key` → same response, no double debit
- [ ] Locking: `SELECT ... FOR UPDATE` on both accounts ordered by ID (prevents deadlock)
- [ ] Atomic: one DB transaction (create entries + transfer record + outbox event)
- [ ] Fee calculation from `fee_rules`
- [ ] Limit check from `limit_rules` (per-operation and daily)
- [ ] `GET /transfers/{id}`
- [ ] **Concurrency test:** 100 parallel transfers from same wallet → balance never negative
- [ ] **Idempotency test:** same key twice → one debit

### 2b — Provider Simulator
**Deliverables:**
- [ ] `POST /v1/charges` — async topup, responds with `provider_ref`
- [ ] `POST /v1/payouts` — async withdrawal
- [ ] `GET /v1/operations/{id}` — status polling endpoint
- [ ] Async webhook delivery with HMAC-SHA256 signature (`X-Signature`, `X-Timestamp`)
- [ ] Test card behaviors (success, decline, slow, duplicate webhook)

### 2c — Funding (Topup & Withdrawal)
**Deliverables:**
- [ ] DB table: `funding_operations`, `outbox_events`
- [ ] `POST /funding/topups` — creates pending operation, calls provider-sim
- [ ] `POST /funding/withdrawals` — reserves funds (wallet → suspense), calls provider-sim
- [ ] `POST /webhooks/provider` — receives webhook, verifies HMAC, processes idempotently
- [ ] On topup success: `external → wallet` entries, status `succeeded`
- [ ] On topup failure: status `failed` with reason
- [ ] On withdrawal success: `suspense → external` entries, status `succeeded`
- [ ] On withdrawal failure: `suspense → wallet` reversal, status `failed`
- [ ] Webhook replay protection (idempotency by provider event ID)
- [ ] Webhook timestamp validation (reject stale webhooks)

### 2d — Worker & Outbox
**Deliverables:**
- [ ] Outbox pattern: events written in same DB transaction as business operation
- [ ] Worker polls `outbox_events`, publishes to Redis queue
- [ ] Worker polls provider-sim for status if webhook not received within timeout
- [ ] Retry logic with exponential backoff

**Stage 2 Acceptance:**
- Top up → transfer → withdraw complete end-to-end
- 100 parallel transfers from one wallet: balance never goes below 0
- Duplicate webhook: second one is a no-op
- Idempotency: repeat POST with same key → original response returned

---

## Stage 3 — Limits, History, Admin, UI
**Goal:** Full MVP. All features wired. UI complete. Deployable.

### 3a — Fees & Limits
**Deliverables:**
- [ ] DB tables: `fee_rules`, `limit_rules`
- [ ] Seed data: default fee and limit values
- [ ] Fee calculation service: fixed and percentage, by operation type
- [ ] Limit check service: per-operation and per-day rolling window
- [ ] Meaningful errors: `LIMIT_EXCEEDED` with `remaining` amount

### 3b — History
**Deliverables:**
- [ ] `GET /transactions` — cursor-paginated list with filters (period, type, status)
- [ ] Search by comment
- [ ] `GET /transactions/{id}` — full details with entries
- [ ] User sees only their own transactions

### 3c — Admin
**Deliverables:**
- [ ] DB table: `audit_log`
- [ ] `GET /admin/users` — search by email or username
- [ ] `GET /admin/users/{id}` — profile, wallets, recent entries
- [ ] `POST /admin/users/{id}/freeze` — freeze wallet, write to audit_log
- [ ] `POST /admin/wallets/{id}/unfreeze`
- [ ] `GET /admin/ledger/transactions` — full ledger view
- [ ] `GET /admin/audit-log`
- [ ] Admin role check on every endpoint
- [ ] Admin can never change balance directly — only via ledger entry

### 3d — Frontend (Client Dashboard)
**Deliverables:**
- [ ] Design system: dark theme, green accent, `Inter` font, Tailwind config
- [ ] Demo banner: «Демо: деньги виртуальные» always visible
- [ ] Auth screens: register, login, email verification
- [ ] Home: balance card, quick actions (Transfer, Top Up), recent transactions
- [ ] Transfer wizard: recipient search → amount + comment → PIN confirmation → receipt
- [ ] Top Up: amount + test card → pending status screen with auto-refresh
- [ ] History: list with filters, transaction detail
- [ ] Profile: PIN change, session list, limits info
- [ ] All loading states: skeletons (not spinners)
- [ ] All empty states with CTAs
- [ ] All error states with human-readable messages

### 3e — Admin UI
**Deliverables:**
- [ ] User search table
- [ ] User card: profile, wallets, entries
- [ ] Freeze/unfreeze with reason
- [ ] Audit log view

### 3f — Deployment
**Deliverables:**
- [ ] VPS deployment with Docker Compose
- [ ] HTTPS via Caddy
- [ ] PostgreSQL backup cron job
- [ ] CI: deploy on push to `main` after green tests
- [ ] Public demo with rate limits on test top-ups

**Stage 3 Acceptance (Full MVP):**
- Two users register, one tops up and transfers to the other, both see it in history
- Transfer requires correct PIN; wrong PIN does not debit
- Repeat request with same `Idempotency-Key` does not debit twice
- 100 parallel transfers don't go negative
- Duplicate provider webhook doesn't create second top-up
- Sum of entries in every transaction = 0
- Limit exceeded → clear error with remaining amount
- Frozen wallet can't send or receive
- Admin freeze action is in audit_log

---

## Stage 4 — Mobile (Future)
**Goal:** Flutter mobile app on top of the existing API.

**Deliverables:**
- [ ] Flutter project setup
- [ ] Auth flows
- [ ] Home screen with balance
- [ ] Transfer and top-up flows
- [ ] History with pull-to-refresh
- [ ] Biometric PIN confirmation

---

## Phase 2 — Extended Features (After MVP, on request)
- USD wallet + UZS↔USD conversion (CBU rates + spread)
- Holds (hold / capture / release)
- 2FA (TOTP)
- Payment requests
- QR code transfers
- KYC levels (Basic / Verified) with limit tiers
- PDF and CSV statements
- Push notifications
- Admin: inline limit and fee editing

## Phase 3 — Advanced (On request)
- Anti-fraud rules and alert queue
- Reconciliation report (sum of all entries = 0 verification)
- Auditor role (read-only)
- Personal finance: categories, budgets, goals, analytics

---

## Open Architecture Decisions (ADR needed before implementation)

| # | Question | Status |
|---|---|---|
| 1 | Sync vs async SQLAlchemy | open |
| 2 | ARQ vs Celery for background tasks | open |
| 3 | Transaction isolation level and locking strategy | open |
| 4 | Balance cache column vs sum-of-entries | open |
| 5 | Default values for fee_rules and limit_rules | open |
| 6 | TTL for idempotency_keys and tokens | open |
| 7 | adjustments account: separate or via suspense | open |
