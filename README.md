# Cloud-Native 3-Tier Incident Management Platform

Beginner-friendly, production-style project to learn DevOps + Cloud + backend infrastructure workflows.

## Project Goal
Build a real-world incident platform while learning:
- 3-tier architecture
- Flask backend fundamentals
- MongoDB Atlas integration
- Redis caching/session/rate-limiting basics
- CI/CD, Docker, Kubernetes, monitoring (next steps)

## Current Progress
- Step 1: Project planning and folder structure
- Step 2: Basic Flask app with UI + health route
- Step 3: MongoDB Atlas integration
- Step 4: Redis integration (cache, session demo, rate limiting)

## Architecture (Current)

Tier 1: UI Layer
- Simple HTML templates served by Flask

Tier 2: Application Layer
- Flask routes and business logic

Tier 3: Data Layer
- MongoDB Atlas for persistent incident data
- Redis (local/cloud) for cache, session, and rate-limit counters

## Folder Structure

```text
cloud-native-incident-platform/
  app/
    templates/
    static/
    routes/
    services/
    models/
    utils/
    __init__.py
  infra/
    docker/
    k8s/
    jenkins/
    monitoring/
    security/
  tests/
  scripts/
  docs/
  app.py
  requirements.txt
  .env.example
  .gitignore
  README.md
```

## Tech Stack (Current)
- Python 3.13+
- Flask
- PyMongo
- MongoDB Atlas
- Redis (local or Redis Cloud)

## Environment Variables
Copy `.env.example` to `.env` and set values:

```env
MONGODB_URI=mongodb+srv://<username>:<password>@<cluster-url>/
MONGODB_DB_NAME=incident_platform

REDIS_HOST=<redis-host>
REDIS_PORT=<redis-port>
REDIS_DB=0
REDIS_USERNAME=default
REDIS_PASSWORD=<redis-password>
REDIS_SSL=true

RATE_LIMIT_REQUESTS=30
RATE_LIMIT_WINDOW_SECONDS=60
```

## Local Run

```powershell
python -m pip install -r requirements.txt
python app.py
```

App URLs (current code):
- UI: `http://127.0.0.1:1000/`
- Health: `http://127.0.0.1:1000/health`

## API Endpoints (Implemented)

### Health
- `GET /health`

### Incident APIs
- `POST /incidents`
- `GET /incidents`
- `PUT /incidents/<title>/status`
- `GET /incidents/search?q=<query>`

### Session Demo APIs (Redis)
- `POST /session/set`
- `GET /session/<user_id>`

## PowerShell API Testing

```powershell
Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:1000/incidents" -ContentType "application/json" -Body '{"title":"API Down","description":"Gateway timeout","status":"open"}'
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:1000/incidents"
Invoke-RestMethod -Method Put -Uri "http://127.0.0.1:1000/incidents/API Down/status" -ContentType "application/json" -Body '{"status":"resolved"}'
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:1000/incidents/search?q=API"

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:1000/session/set" -ContentType "application/json" -Body '{"user_id":"u1","role":"admin"}'
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:1000/session/u1"
```

## Troubleshooting

### `TemplateNotFound: index.html`
Flask template path mismatch. Ensure `app.py` sets:
- `template_folder="app/templates"`

### Redis shows `error` in `/health`
- Check host/port
- Check username/password
- Ensure TLS if cloud (`REDIS_SSL=true`)

### MongoDB connection issues
- Validate Atlas DB user permissions
- Allow current IP in Atlas Network Access
- URL-encode special characters in password

### `REDIS_DB` ValueError
- Must be numeric (`0`, `1`, etc.)

## Why This Project Matters for Jobs
This project demonstrates:
- backend + data-store integration
- cloud service configuration discipline via env vars
- cache and rate-limit patterns used in production
- clean project structure for CI/CD and Kubernetes expansion

## Next Planned Steps
- Step 5: Docker fundamentals
- Step 6: Docker Compose
- Step 7+: GitHub workflow, Jenkins CI/CD, webhooks, Trivy, Kubernetes, monitoring

## Recommended Official Docs
- Flask: https://flask.palletsprojects.com/
- PyMongo: https://www.mongodb.com/docs/drivers/pymongo/
- MongoDB Atlas: https://www.mongodb.com/docs/atlas/
- Redis Python client: https://redis.readthedocs.io/
