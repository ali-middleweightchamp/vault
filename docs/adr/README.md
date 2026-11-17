# Architecture Decision Records

This directory contains ADRs for Vault.

## Format

Each ADR is a markdown file: `NNNN-short-title.md`

```markdown
# NNNN — Title

**Date:** YYYY-MM-DD
**Status:** proposed | accepted | superseded

## Context
What is the problem or decision to be made?

## Decision
What was decided?

## Rationale
Why this choice over the alternatives?

## Consequences
What becomes easier or harder?
```

## Status values

`proposed` → `accepted` → `superseded`

## Open decisions (need ADR before implementation)

1. Sync vs async SQLAlchemy
2. ARQ vs Celery for background tasks
3. Transaction isolation level and locking strategy for transfers
4. Balance cache column vs sum-of-entries
5. Default values for `fee_rules` and `limit_rules`
6. TTL for `idempotency_keys` and token lifetimes
7. `adjustments` account: separate ledger account or via `suspense`
