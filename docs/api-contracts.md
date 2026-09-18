# API contracts

The public API is exposed by Kong at `http://localhost:8080`. Internal service ports remain published for development and OpenAPI inspection.

| Public prefix | Upstream |
| --- | --- |
| `/api/auth` | Auth service `/auth` |
| `/api/cases` | Case service `/cases` |
| `/api/ai` | AI service `/` |
| `/api/knowledge` | Knowledge service `/` |
| `/api/automation` | Automation service `/` |

## Auth service — `:8005`

- `GET /health` — service status.
- `POST /auth/dev-token` — issues a one-hour opaque development token when `AUTH_MODE=development`.
- `GET /auth/me` — resolves the bearer token to its development user.
- `DELETE /auth/session` — revokes the bearer token.

Development tokens are intentionally local and in memory. Production authentication must validate Keycloak-issued tokens instead of enabling this endpoint.

## Case service — `:8001`

- `GET /health` — service status.
- `GET /cases` — list cases.
- `POST /cases` — `{ "title": string, "summary": string }`; returns `201` case.
- `GET /cases/{id}` — case detail or `404`.
- `POST /cases/{id}/approve` — `{ "note": string }`; requires `x-user-role: approver|admin` and returns the approved case.

## AI service — `:8002`

- `GET /health` — service status.
- `POST /diagnose` — `{ "case_id": string, "question": string }`; returns `{ case_id, diagnosis, sources }`.

## Knowledge service — `:8003`

- `GET /health` — service status.
- `POST /documents` — `{ "title": string, "content": string }`; embeds and stores a document.
- `GET /search?q=...` — ranked results with `id`, `title`, `content`, and `score`.

## Automation service — `:8004`

- `GET /health` — service status.
- `GET /actions` — safe whitelisted actions.
- `POST /executions` — `{ "action": string, "target_container": string }`; returns an audit record. Default status is `dry-run`.
- `GET /executions` — in-memory execution audit list.

FastAPI publishes interactive OpenAPI documentation at `/docs` on each service port.
