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
- Step 12: Monitoring stack on Kubernetes (Prometheus + Grafana)
- Step 13: Advanced Kubernetes ops (replicas, rolling updates, config/secrets, probes)

## Architecture (Current)

Tier 1: UI Layer
- Simple HTML templates served by Flask

Tier 2: Application Layer
- Flask routes and business logic
- `/metrics` endpoint for Prometheus scraping

Tier 3: Data Layer
- MongoDB for persistent incident data
- Redis (local/cloud) for cache, session, and rate-limit counters

## Folder Structure

```text
cloud-native-incident-platform/
  app/
  infra/
    docker/
    jenkins/
    k8s/
      namespace.yaml
      mongo.yaml
      redis.yaml
      app.yaml
      app-configmap.yaml
      app-secret.yaml
    monitoring/
      prometheus-configmap.yaml
      prometheus.yaml
      grafana-datasource-configmap.yaml
      grafana.yaml
    security/
  docs/
    jenkins-setup.md
    github-webhook-setup.md
    k8s-minikube-setup.md
    monitoring-setup.md
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
- Jenkins (Pipeline)
- Kubernetes (Minikube + kubectl)
- Prometheus + Grafana
- Trivy

## Kubernetes (Step 11 + Step 13)

Base manifests:
- `infra/k8s/namespace.yaml`
- `infra/k8s/mongo.yaml`
- `infra/k8s/redis.yaml`
- `infra/k8s/app.yaml`

Advanced config manifests:
- `infra/k8s/app-configmap.yaml` (non-secret app settings)
- `infra/k8s/app-secret.yaml` (secret placeholders)

Step 13 improvements now implemented:
- App replicas increased to `2`
- Rolling update strategy enabled (`maxSurge: 1`, `maxUnavailable: 0`)
- Readiness and liveness probes on `/health`
- App env moved to ConfigMap/Secret refs (`envFrom`)

## Monitoring (Step 12)

Applied manifests:
- `infra/monitoring/prometheus-configmap.yaml`
- `infra/monitoring/prometheus.yaml`
- `infra/monitoring/grafana-datasource-configmap.yaml`
- `infra/monitoring/grafana.yaml`

## Trivy Results (Current)
- Trivy scan integrated in Jenkins pipeline.
- Current image scan reports 4 HIGH vulnerabilities (ncurses family).
- Pipeline is in report-only mode (`--exit-code 0`) for learning stage.

## API Endpoints (Implemented)
- `GET /`
- `GET /health`
- `GET /metrics`
- `POST /incidents`
- `GET /incidents`
- `PUT /incidents/<title>/status`
- `GET /incidents/search?q=<query>`
- `POST /session/set`
- `GET /session/<user_id>`

## Next Planned Steps
- Step 14: Final architecture review and interview-ready explanation

## Recommended Official Docs
- Kubernetes: https://kubernetes.io/docs/home/
- Prometheus: https://prometheus.io/docs/introduction/overview/
- Grafana: https://grafana.com/docs/
- Jenkins Pipeline: https://www.jenkins.io/doc/book/pipeline/
- Trivy: https://trivy.dev/latest/docs/
