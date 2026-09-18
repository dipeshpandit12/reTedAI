# Docker development guide

Docker Compose is the canonical runtime for reTedAI. Host-based commands are optional conveniences; a change is not considered runnable until its image builds and its container-level checks pass.

## Prerequisites

- Docker Desktop or Docker Engine with Compose v2.
- Ports `3000`, `5432`, `5672`, `8001`–`8006`, `8080`, and `15672` available.
- At least 4 GB of memory available to Docker for the complete local stack.

## First startup

```bash
cp .env.example .env
docker compose config --quiet
docker compose up --build -d --wait --wait-timeout 120
docker compose ps
python db/seed/load_seed.py
python scripts/smoke_test.py
```

A successful `docker compose ps` shows every container as `healthy`. The smoke test prints JSON with `"status": "ok"` after it enters through Kong, renders the Next.js page, creates and approves a case through Kong, and searches knowledge.

## Start one service

Compose automatically starts declared dependencies:

| Command | Starts |
| --- | --- |
| `docker compose up --build auth` | Auth, PostgreSQL |
| `docker compose up --build case` | Case, PostgreSQL, RabbitMQ |
| `docker compose up --build knowledge` | Knowledge, PostgreSQL |
| `docker compose up --build ai` | AI, knowledge, PostgreSQL |
| `docker compose up --build automation` | Automation, PostgreSQL |
| `docker compose up --build web` | Web, case, knowledge, PostgreSQL, RabbitMQ |
| `docker compose up --build kong` | Complete public application stack |

To prove that a service's starter image boots without dependencies, run its image directly:

```bash
docker build -t retedai-case ./services/case
docker run --rm -p 8001:8001 retedai-case
```

Use `retedai-ai:8002`, `retedai-knowledge:8003`, `retedai-automation:8004`, or `retedai-auth:8005` for the other services. The AI service falls back locally when no model key or knowledge service is available. Auth starts with development token issuance disabled unless `AUTH_MODE=development`. Case, auth, and knowledge use in-memory repositories until PostgreSQL persistence is implemented. Automation returns audited dry runs unless explicitly enabled.

## Container-level tests

Tests are copied into each service image and run as the non-root application user:

```bash
docker compose build auth case ai knowledge automation
docker compose run --rm --no-deps auth python -m pytest -q
docker compose run --rm --no-deps case python -m pytest -q
docker compose run --rm --no-deps ai python -m pytest -q
docker compose run --rm --no-deps knowledge python -m pytest -q
docker compose run --rm --no-deps automation python -m pytest -q
```

`--no-deps` proves each unit-test suite is isolated from live PostgreSQL, RabbitMQ, and external model providers.

## Logs and troubleshooting

```bash
docker compose ps
docker compose logs -f web
docker compose logs -f kong
docker compose logs -f auth case ai knowledge automation
docker compose logs --since=10m
```

Common issues:

- **Port already allocated:** stop the process using the listed host port or change the left side of its mapping in `docker-compose.yml`.
- **A service remains unhealthy:** inspect `docker compose logs <service>` and run its `/health` endpoint from inside the container.
- **Kong returns 404:** validate `gateway/kong.yml` and confirm the request uses the documented `/api/...` prefix.
- **Docker Hub credential helper hangs on public images:** confirm Docker Desktop is fully started, sign in again, or fix the local Docker credential-store configuration. Do not commit machine-specific Docker configuration.
- **No cases after restart:** the starter case and knowledge repositories are in memory. Run `python db/seed/load_seed.py` after service recreation.
- **Provider requests fail:** leave model keys empty to use the deterministic AI fallback, or verify the relevant key/model variables in `.env`.
- **Automation does not execute:** this is expected. `ENABLE_AUTOMATION_EXECUTION=false` is the safe default, and the base starter image does not expose the Docker socket.

## Stop or reset

Stop containers while preserving PostgreSQL data:

```bash
docker compose down
```

Deleting the database is destructive and should be deliberate:

```bash
docker compose down --volumes
```

Never use the volume-deleting command against an environment whose data must be retained.
