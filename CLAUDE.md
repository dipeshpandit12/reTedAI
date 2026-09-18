# reTedAI AI repository guide

Read this file before editing, running, testing, committing, or proposing changes.

## Repository model

- `gateway/kong.yml` is the production-like public routing boundary. Kong runs DB-less and exposes the application on port 8080.
- `web/` is a Next.js 16 TypeScript App Router application. Its `app/api/` route handlers are a direct-port development fallback, not the primary Compose gateway.
- `services/auth/` owns development sessions and the future Keycloak token-verification boundary. Development tokens must never become a production authentication mechanism.
- `services/case/` owns case state, comments, actions, approval, and the future RabbitMQ publisher.
- `services/ai/` owns retrieval orchestration, prompts, and Anthropic/OpenAI calls. It has no database.
- `services/knowledge/` owns documents, chunks, embeddings, and hybrid search.
- `services/automation/` owns the only action whitelist, execution seam, and audit records. Execution is disabled by default.
- `db/` owns PostgreSQL schemas, pgvector initialization, and demo seed data.
- `docker-compose.yml` is the supported full-stack local entry point.

Services must communicate over HTTP or events. Never import one service's Python package from another service.

## Safety and current seams

The repositories in `auth`, `case`, `knowledge`, and `automation` are in-memory development implementations even though PostgreSQL is provisioned. Preserve their interfaces when adding persistence. The case event emitter logs an envelope until RabbitMQ publishing is implemented. Automation must remain deny-by-default: add actions only in `services/automation/app/whitelist.py`, validate target names, keep audit records, and never accept arbitrary shell commands.

Never commit secrets, `.env`, `.venv`, `node_modules`, `.next`, caches, coverage, or provider responses containing sensitive data.

## Run the full stack

```bash
cp .env.example .env
docker compose up --build
python db/seed/load_seed.py
```

| Component | Address |
| --- | --- |
| Kong application entry point | `http://localhost:8080` |
| Kong admin API (local only) | `http://localhost:8006` |
| Direct Next.js development port | `http://localhost:3000` |
| Case/OpenAPI | `http://localhost:8001/docs` |
| AI/OpenAPI | `http://localhost:8002/docs` |
| Knowledge/OpenAPI | `http://localhost:8003/docs` |
| Automation/OpenAPI | `http://localhost:8004/docs` |
| Auth/OpenAPI | `http://localhost:8005/docs` |
| RabbitMQ management | `http://localhost:15672` |

Use `docker compose down` to stop without deleting data. Never add `-v` unless the user explicitly wants database data deleted.

## Run components independently

Docker is the canonical runtime. Use Compose to start one service and its declared dependencies:

```bash
docker compose up --build case
docker compose up --build auth
docker compose up --build ai
docker compose up --build knowledge
docker compose up --build automation
docker compose up --build web
```

The service images copy their test suites, so container-level tests must work:

```bash
docker compose run --rm auth python -m pytest -q
docker compose run --rm case python -m pytest -q
docker compose run --rm ai python -m pytest -q
docker compose run --rm knowledge python -m pytest -q
docker compose run --rm automation python -m pytest -q
```

After the full stack and seed loader are running, execute `python scripts/smoke_test.py`. It must enter through Kong, render the Next.js home page, create/get/approve a case through Kong's service route, and search knowledge.

Host-based commands are for development convenience only.

Web:

```bash
cd web
npm ci
npm run dev
```

Each Python service follows the same workflow. Use ports 8001/8002/8003/8004/8005 for case/ai/knowledge/automation/auth:

```bash
cd services/case
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8001
```

## Test and validation rules

Run a service suite from its own directory so `app` resolves correctly:

```bash
cd services/case
python -m pytest -q
```

Minimum validation before a PR to `dev`:

```bash
cd web && npm ci && npm run build && cd ..
for service in services/*; do (cd "$service" && python -m pytest -q); done
docker compose config --quiet
python -m compileall -q services db/seed
python scripts/smoke_test.py
```

New endpoints require success, validation, authorization, and not-found tests where applicable. Mock external providers and network calls. Tests must not require live Anthropic, OpenAI, RabbitMQ, or PostgreSQL instances unless explicitly marked as integration tests.

For Next.js, keep Server Components as the default, use `"use client"` only for browser interaction, await dynamic `params`, and keep backend credentials in server-only variables. Browser code must use relative `/api/...` paths: Kong handles them in Compose, while `app/api/` provides the direct-port development fallback.

For the Compose application, browser `/api/*` calls are matched by Kong before the catch-all web route. Keep `gateway/kong.yml` and the Next.js fallback handlers behaviorally compatible. Authentication headers injected by Kong are development seams only; replace them with verified identity claims before deployment.

## GitHub and branch policy

This repository uses GitHub Actions in `.github/workflows/ci.yml`; do not add Bitbucket configuration.

- `main` and `dev` are protected; never push directly to either branch.
- `dev` contains only runnable commits that pass GitHub Actions.
- Create contributor branches from the latest `dev`: `feature/<name>/<topic>`, `fix/<name>/<topic>`, `docs/<name>/<topic>`, `test/<name>/<topic>`, or `chore/<name>/<topic>`.
- Before opening or updating a PR, run `git fetch origin` then `git rebase origin/dev`, resolve conflicts, and rerun validation.
- Target `dev` from contributor branches. Promote `dev` to `main` only through a reviewed release PR after the dev environment is verified.
- Use rebase-and-merge or squash-and-merge. If a rebased contributor branch must be updated remotely, use `--force-with-lease`, never `--force`.
- AI assistants must not commit, push, merge, or open PRs without explicit user authorization and must not alter Git identity.

Use Conventional Commits:

```text
feat(case): add persisted case repository
fix(web): forward approval errors
test(knowledge): cover keyword fallback
docs(repo): update local run guide
ci(github): validate service matrix
```

## Definition of done

A change is ready when it follows component ownership, includes relevant tests, passes the required validation, updates contracts and environment examples, contains no secrets or generated artifacts, is rebased on current `origin/dev`, and targets `dev` through a reviewed PR.
