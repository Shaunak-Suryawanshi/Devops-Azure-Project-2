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
- Step 5: Docker fundamentals (Docker image build/run lifecycle)
- Step 6: Docker Compose (modular multi-service setup)
- Step 7: Git + GitHub workflow (main-only practical flow)
- Step 8: Jenkins Pipeline CI/CD setup (basic build-deploy-smoke-test)

## Architecture (Current)

Tier 1: UI Layer
- Simple HTML templates served by Flask

Tier 2: Application Layer
- Flask routes and business logic

Tier 3: Data Layer
- MongoDB for persistent incident data
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
      app/
        Dockerfile
        .dockerignore
      compose/
        docker-compose.app.yml
        docker-compose.mongo.yml
        docker-compose.redis.yml
    jenkins/
      Jenkinsfile
    k8s/
    monitoring/
    security/
  tests/
  scripts/
  docs/
    jenkins-setup.md
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
- Docker
- Docker Compose
- Jenkins (Pipeline)

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

For Jenkins pipeline runs, set these in Jenkins job/global environment as well.

## Local Run (Without Docker)

```powershell
python -m pip install -r requirements.txt
python app.py
```

App URLs:
- UI: `http://127.0.0.1:1000/`
- Health: `http://127.0.0.1:1000/health`

## Docker Compose (Modular)

This project uses three separate compose files:
- `docker-compose.mongo.yml` for MongoDB service
- `docker-compose.redis.yml` for Redis service
- `docker-compose.app.yml` for Flask app service

Run all services together:

```powershell
docker compose -f infra/docker/compose/docker-compose.mongo.yml -f infra/docker/compose/docker-compose.redis.yml -f infra/docker/compose/docker-compose.app.yml up -d --build
```

Check status:

```powershell
docker compose -f infra/docker/compose/docker-compose.mongo.yml -f infra/docker/compose/docker-compose.redis.yml -f infra/docker/compose/docker-compose.app.yml ps
```

Stop all services:

```powershell
docker compose -f infra/docker/compose/docker-compose.mongo.yml -f infra/docker/compose/docker-compose.redis.yml -f infra/docker/compose/docker-compose.app.yml down
```

## Jenkins Pipeline (Step 8)

Pipeline file:
- `infra/jenkins/Jenkinsfile`

What pipeline currently does:
- Checkout code
- Check Docker availability
- Build Docker image
- Remove old container if exists
- Run new container with env vars
- Smoke test `/health`

Detailed guide:
- `docs/jenkins-setup.md`

## API Endpoints (Implemented)
- `GET /health`
- `POST /incidents`
- `GET /incidents`
- `PUT /incidents/<title>/status`
- `GET /incidents/search?q=<query>`
- `POST /session/set`
- `GET /session/<user_id>`

## Troubleshooting

### `TemplateNotFound: index.html`
Ensure Flask app is configured with:
- `template_folder="app/templates"`

### Redis shows `error` in `/health`
- Check host, port, username, password
- Ensure TLS if cloud: `REDIS_SSL=true`

### MongoDB connection issues
- Validate Atlas DB user permissions
- Allow current IP in Atlas Network Access
- URL-encode special characters in password

### `REDIS_DB` ValueError
- Must be numeric (`0`, `1`, etc.)

### Jenkins build fails on Docker
- Ensure Docker Desktop is running
- Ensure Jenkins service user can access Docker
- Check `docker --version` stage output in build logs

## Why This Project Matters for Jobs
This project demonstrates:
- backend + data-store integration
- cloud service configuration using env vars
- cache and rate-limiting production patterns
- modular infra layout used in real teams
- basic CI/CD automation using Jenkins pipeline-as-code

## Next Planned Steps
- Step 9: GitHub Webhooks
- Step 10+: Trivy, Kubernetes, monitoring

## Recommended Official Docs
- Flask: https://flask.palletsprojects.com/
- PyMongo: https://www.mongodb.com/docs/drivers/pymongo/
- MongoDB Atlas: https://www.mongodb.com/docs/atlas/
- Redis Python client: https://redis.readthedocs.io/
- Docker Compose: https://docs.docker.com/compose/
- Jenkins Pipeline: https://www.jenkins.io/doc/book/pipeline/
