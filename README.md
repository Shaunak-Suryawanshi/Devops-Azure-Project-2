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
- Step 10: Trivy image scanning integrated in Jenkins
- Step 11: Kubernetes deployment on Minikube (3-tier running)

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
      namespace.yaml
      mongo.yaml
      redis.yaml
      app.yaml
    monitoring/
    security/
  tests/
  scripts/
  docs/
    jenkins-setup.md
    github-webhook-setup.md
    k8s-minikube-setup.md
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
- Kubernetes (Minikube + kubectl)
- Trivy

## Local Run (Without Docker)

```powershell
python -m pip install -r requirements.txt
python app.py
```

App URLs:
- UI: `http://127.0.0.1:1000/`
- Health: `http://127.0.0.1:1000/health`

## Docker Compose (Modular)

```powershell
docker compose -f infra/docker/compose/docker-compose.mongo.yml -f infra/docker/compose/docker-compose.redis.yml -f infra/docker/compose/docker-compose.app.yml up -d --build
```

## Jenkins + Webhook

- Pipeline file: `infra/jenkins/Jenkinsfile`
- Webhook URL format: `https://<ngrok-url>/github-webhook/`
- Pipeline currently includes Docker build + Trivy scan + deploy + smoke test.

Docs:
- `docs/jenkins-setup.md`
- `docs/github-webhook-setup.md`

## Kubernetes (Step 11)

Applied manifests:
- `infra/k8s/namespace.yaml`
- `infra/k8s/mongo.yaml`
- `infra/k8s/redis.yaml`
- `infra/k8s/app.yaml`

Current verified state:
- `incident-app` pod running
- `mongo` pod running
- `redis` pod running
- Service health reachable and app working via Minikube

Kubernetes guide:
- `docs/k8s-minikube-setup.md`

## Trivy Results (Current)
- Trivy stage is active in Jenkins.
- Current image scan reports 4 HIGH vulnerabilities (ncurses packages in base OS).
- Pipeline is set to report-only mode (`--exit-code 0`) for learning stage.

## API Endpoints (Implemented)
- `GET /health`
- `POST /incidents`
- `GET /incidents`
- `PUT /incidents/<title>/status`
- `GET /incidents/search?q=<query>`
- `POST /session/set`
- `GET /session/<user_id>`

## Next Planned Steps
- Step 12: Monitoring stack (Prometheus + Grafana)
- Step 13: Advanced DevOps concepts (scaling, rolling updates, env/secrets)
- Step 14: Final architecture review

## Recommended Official Docs
- Flask: https://flask.palletsprojects.com/
- PyMongo: https://www.mongodb.com/docs/drivers/pymongo/
- MongoDB Atlas: https://www.mongodb.com/docs/atlas/
- Redis Python client: https://redis.readthedocs.io/
- Docker Compose: https://docs.docker.com/compose/
- Jenkins Pipeline: https://www.jenkins.io/doc/book/pipeline/
- GitHub Webhooks: https://docs.github.com/en/webhooks
- Trivy: https://trivy.dev/latest/docs/
- Kubernetes: https://kubernetes.io/docs/home/
- Minikube: https://minikube.sigs.k8s.io/docs/
