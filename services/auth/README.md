# Auth Service

The auth service is the identity boundary for reTedAI. It accepts authentication credentials, resolves the current user, and exposes a normalized user representation to the application.

For the broader ownership model, see [Authentication Architecture](../../docs/auth-architecture.md).

## Purpose

### Already implemented

- Runs as a FastAPI service on port `8005`.
- Provides a local development session store.
- Issues random bearer tokens when development authentication is explicitly enabled.
- Resolves a bearer token to the current user.
- Revokes development sessions.
- Returns `401 Unauthorized` for missing or invalid/expired bearer tokens.

### Planned

- Validate Keycloak access tokens using the configured issuer and signing keys.
- Map verified Keycloak claims to the application's normalized user model.
- Coordinate provider-backed login and logout behavior.
- Become the shared authentication boundary used by every backend service.

The auth service does not own domain permissions. Case, AI, knowledge, and automation services remain responsible for deciding whether an authenticated user may perform their operations.

## Current status

| Capability | Status | Details |
| --- | --- | --- |
| Development sessions | **Implemented** | In-memory sessions with a one-hour token lifetime. |
| Development token issuance | **Implemented** | Available only when `AUTH_MODE=development`; disabled otherwise. |
| Current-user lookup | **Implemented** | `/auth/me` resolves development bearer tokens. |
| Session revocation | **Implemented** | `DELETE /auth/session` removes a development session. |
| Keycloak token verification | **Planned** | `KEYCLOAK_*` settings exist as configuration placeholders, but verification is not wired in. |
| Persistent sessions/users | **Planned** | Current sessions are lost when the auth process restarts. |
| Production login/logout flow | **Planned** | Keycloak will own credentials, login, roles, and provider sessions. |

## Architecture

The intended boundary is:

1. Keycloak, or the explicit development substitute, establishes the user's identity.
2. The auth service verifies the bearer token and returns normalized user information.
3. The domain service checks permissions for its own operation.
4. The domain service returns `401` for an unauthenticated request or `403` for an authenticated user without permission.

The production Keycloak path is **planned**. The currently implemented path is the in-memory development session store.

See [Authentication Architecture](../../docs/auth-architecture.md) for the request-flow diagram and migration plan.

## Endpoints

### `GET /health` and `GET /auth/health`

**Implemented.** Return service health:

```json
{"status":"ok","service":"auth"}
```

### `POST /auth/dev-token`

**Implemented for development only.** Issues a development bearer token when `AUTH_MODE=development`.

Example request:

```json
{
  "email": "reviewer@retedai.local",
  "name": "Demo Reviewer",
  "role": "approver"
}
```

The response contains `access_token`, `token_type`, `expires_in`, and the normalized `user`. The default request values are demo-oriented and must not be used as production identity data.

When development mode is disabled, the endpoint returns `404`.

### `GET /auth/me`

**Implemented for development tokens.** Requires:

```http
Authorization: Bearer <access-token>
```

Returns the normalized user:

```json
{
  "id": "user-id",
  "email": "user@example.com",
  "name": "User Name",
  "role": "analyst"
}
```

Keycloak token support for this endpoint is **planned**.

### `DELETE /auth/session`

**Implemented for development sessions.** Requires the same bearer token and revokes that token. A later `/auth/me` request with the token returns `401`.

Provider-backed Keycloak logout is **planned** and will use the Keycloak logout/end-session flow in addition to clearing the application's local session state.

## Roles

The currently supported role values are:

- `analyst`
- `approver`
- `admin`

### Already implemented

Development token requests validate the role against these values, and the role is returned as part of the normalized user.

### Planned

Keycloak role or group claims will be mapped to these application roles. Each domain service will enforce permissions for its own operations; possessing a role does not automatically authorize every operation or resource.

## Configuration

### Existing variables

These variables are present in `services/auth/.env.example`:

| Variable | Current meaning | Status |
| --- | --- | --- |
| `AUTH_MODE` | Set to `development` to enable `/auth/dev-token`; any other value disables it. | **Implemented** |
| `DATABASE_URL` | Database connection placeholder for future persistence. | **Declared; not used by current in-memory sessions** |
| `KEYCLOAK_URL` | Keycloak base URL placeholder. | **Declared; verification planned** |
| `KEYCLOAK_REALM` | Keycloak realm name, defaulting to `retedai`. | **Declared; verification planned** |
| `KEYCLOAK_CLIENT_ID` | Keycloak client ID, defaulting to `retedai-web`. | **Declared; verification planned** |

### Proposed variables for Keycloak verification

These variables are **planned** and should be supplied through deployment configuration when Keycloak verification is implemented:

- `KEYCLOAK_ISSUER`: trusted issuer URL, preferably derived from the realm URL.
- `KEYCLOAK_AUDIENCE`: expected access-token audience.
- `KEYCLOAK_JWKS_URL`: signing-key endpoint, or an equivalent discovery setting.
- `KEYCLOAK_ROLE_CLAIM`: claim path containing application roles.
- `AUTH_CLOCK_SKEW_SECONDS`: permitted clock skew when validating time claims.

Secrets, client credentials, and signing material must not be committed to this repository. Access tokens and refresh tokens must not be logged.

## Running locally

The canonical local runtime is Docker Compose.

Start the auth service and its declared dependencies:

```bash
docker compose up --build auth
```

Run it in the background and wait for health checks:

```bash
docker compose up --build -d --wait auth
```

The service is available at `http://localhost:8005`. Health checks are available at:

```text
http://localhost:8005/health
http://localhost:8005/auth/health
```

To enable development token issuance, set `AUTH_MODE=development` in the environment used by Compose. It is disabled by default unless explicitly configured.

## Testing

Run the auth tests in the service image:

```bash
docker compose build auth
docker compose run --rm --no-deps auth python -m pytest -q
```

Expected outcome: all tests pass, including health checks, confirmation that development tokens are disabled by default, and the development session lifecycle (issue, resolve, revoke, then reject).

For a host-based test run after installing `services/auth/requirements.txt`:

```bash
cd services/auth
python -m pytest -q
```

Keycloak verification tests are **planned**. They should cover valid claims, wrong issuer or audience, invalid signatures, expired tokens, missing roles, and insufficient permissions at the owning domain service.

## Integration contract

### Input

The planned common input is:

```http
Authorization: Bearer <access-token>
```

The currently implemented development path accepts the same header format for tokens issued by `/auth/dev-token`.

Backends must not treat browser-provided `x-user-id` or `x-user-role` headers as proof of identity. The existing header-based development seams are temporary and must be removed when bearer-token verification is connected throughout the stack.

### Verified user response

The auth boundary returns a normalized user with:

```json
{
  "id": "stable-user-id",
  "email": "user@example.com",
  "name": "User Name",
  "role": "analyst"
}
```

For Keycloak, `id` should come from the verified stable subject claim, normally `sub`; roles must come from verified provider claims rather than request input.

### Errors

- `401 Unauthorized`: the bearer token is missing, malformed, invalid, expired, or issued by an untrusted provider.
- `403 Forbidden`: the identity is valid, but the owning domain service rejects the requested operation due to insufficient permission.
- `404 Not Found` on `/auth/dev-token`: development token issuance is disabled.

Error responses should not expose detailed token-validation reasons, and logs must never contain credentials or access tokens.

## Limitations and migration notes

### Already implemented limitations

- Sessions are stored in memory and disappear when the auth process restarts.
- Development tokens are not Keycloak tokens and do not exercise provider login, refresh, or logout.
- `/auth/dev-token` has demo-oriented defaults: `demo@retedai.local`, `Demo Analyst`, and `approver`.
- The web session fallback currently uses `demo-user` and `Demo Analyst`.
- Kong currently injects `x-user-id:demo-user` and `x-user-role:approver` for the case route.
- The case service currently accepts default or supplied identity headers through its development dependency.

### Planned removals

- Remove fixed demo identities and require an explicit development token or a verified Keycloak session.
- Replace identity headers with bearer-token propagation and verified claims.
- Implement Keycloak signature, issuer, audience, expiration, and role-claim validation.
- Add persistent user/session handling only if the application requires it; Keycloak remains the authority for credentials and provider sessions.
