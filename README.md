# GEO SaaS

Minimal MVP scaffold for Generative Engine Optimization platform.

## Components

- **backend/** – FastAPI microservice exposing REST API
- **db** – PostgreSQL (via docker-compose)
- **worker/** – (to be implemented) async workers for crawling & analysis
- **frontend/** – (to be implemented) Next.js UI

## Quick start

```bash
git clone <repo>
cd repo
# start services
docker-compose up --build
```

API will be available at http://localhost:8000 (see `/docs` for Swagger UI).

Database connection string defaults to `postgresql+asyncpg://postgres:postgres@localhost:5432/geo`.

## Development

Back-end live reload enabled through `--reload` in docker-compose.

Create a site:

```bash
curl -X POST http://localhost:8000/sites -H 'Content-Type: application/json' -d '{"domain": "example.com"}'
```