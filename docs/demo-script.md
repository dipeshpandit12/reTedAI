# Demo script

1. Run `docker compose up --build` and wait for healthy services.
2. Run `python db/seed/load_seed.py`.
3. Run `python scripts/smoke_test.py` and confirm its JSON status is `ok`.
4. Open `http://localhost:8080`; explain that Kong is the public entry point and show the seeded case list.
5. Open `http://localhost:8005/docs` and demonstrate development token issuance plus `/auth/me`; explain the Keycloak seam.
6. Select **New case**, enter a title and summary, and submit.
7. Open the created case and explain the diagnosis approval and timeline areas.
8. Select **Knowledge**, search for `database latency`, and show ranked past-case/runbook results.
9. Open `http://localhost:8002/docs` and run `POST /diagnose` to demonstrate the local fallback or configured provider.
10. Open `http://localhost:8004/docs`, list actions, and submit `disk_usage` against `case`; point out the audited `dry-run` result.
11. Explain that enabling real automation requires an explicit environment flag plus Docker execution capability and remains restricted to the whitelist.
