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
- Step 8: Jenkins Pipeline CI/CD setup (build, deploy, smoke test)
- Step 9: GitHub Webhook auto-trigger with ngrok

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
    github-webhook-setup.md
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
- GitHub Webhooks
- ngrok

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

For Jenkins runs, secret values should come from Jenkins Credentials.

## Local Run (Without Docker)

```powershell
python -m pip install -r requirements.txt
python app.py
```

App URLs:
- UI: `http://127.0.0.1:1000/`
- Health: `http://127.0.0.1:1000/health`

## Docker Compose (Modular)

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
- Run new container on host port `1001`
- Smoke test `/health`

Detailed guide:
- `docs/jenkins-setup.md`

## GitHub Webhook (Step 9)

Current flow:
- GitHub push triggers Jenkins automatically
- Webhook endpoint is exposed with ngrok

Detailed guide:
- `docs/github-webhook-setup.md`

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
Ensure Flask app uses `template_folder="app/templates"`.

### Redis shows `error` in `/health`
- Check host, port, password, ssl mode.
- For Redis Cloud, usually set `REDIS_SSL=true` and cloud host/port.

### MongoDB connection issues
- Validate Atlas DB user permissions.
- Allow current IP in Atlas Network Access.
- URL-encode special characters in password.

### Jenkins build fails
- Ensure Docker Desktop is running.
- Ensure Jenkins service user can access Docker.
- Check `docker --version` stage output.

### Webhook does not trigger
- Verify Jenkins job option `GitHub hook trigger for GITScm polling` is enabled.
- Verify webhook URL ends with `/github-webhook/`.
- Keep ngrok tunnel running.

## Why This Project Matters for Jobs
This project demonstrates:
- backend + data-store integration
- cloud service configuration using env vars and credentials
- cache and rate-limiting production patterns
- modular infra layout used in real teams
- CI/CD automation with Jenkins and GitHub webhooks

## Next Planned Steps
- Step 10: Trivy security scanning
- Step 11+: Kubernetes and monitoring

## Recommended Official Docs
- Flask: https://flask.palletsprojects.com/
- PyMongo: https://www.mongodb.com/docs/drivers/pymongo/
- MongoDB Atlas: https://www.mongodb.com/docs/atlas/
- Redis Python client: https://redis.readthedocs.io/
- Docker Compose: https://docs.docker.com/compose/
- Jenkins Pipeline: https://www.jenkins.io/doc/book/pipeline/
- GitHub Webhooks: https://docs.github.com/en/webhooks
- ngrok: https://ngrok.com/docs
