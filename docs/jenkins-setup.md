# Jenkins Setup and Runbook (Step 8)

This guide explains how to run the project CI/CD pipeline on Windows Jenkins.

## Pipeline Type
Use **Pipeline Job** (not Freestyle).

## Jenkinsfile Location
`infra/jenkins/Jenkinsfile`

## Create Jenkins Pipeline Job
1. Open Jenkins UI: `http://localhost:8080`
2. New Item -> choose **Pipeline**
3. In job config:
- Definition: `Pipeline script from SCM`
- SCM: `Git`
- Repository URL: your GitHub repo URL
- Branch: `main`
- Script Path: `infra/jenkins/Jenkinsfile`
4. Save.

## Required Environment Variables
Configure these in Jenkins (job config or global env):
- `MONGODB_URI`
- `MONGODB_DB_NAME`
- `REDIS_HOST`
- `REDIS_PORT`
- `REDIS_DB`
- `REDIS_USERNAME`
- `REDIS_PASSWORD`
- `REDIS_SSL`
- `RATE_LIMIT_REQUESTS`
- `RATE_LIMIT_WINDOW_SECONDS`

## Pipeline Stages and Purpose
1. `Checkout Code`: pulls latest source from GitHub.
2. `Docker Version Check`: confirms Docker is usable on Jenkins host.
3. `Build Docker Image`: builds app image with build number and `latest` tags.
4. `Stop Old Container`: removes existing deployment container if present.
5. `Run New Container`: starts new container with env vars.
6. `Smoke Test`: calls `/health` endpoint to verify deployment.

## Build Validation Commands (PowerShell)
After Jenkins build succeeds, verify:

```powershell
docker ps --filter "name=incident-platform-ci"
Invoke-RestMethod -Method Get -Uri "http://127.0.0.1:1000/health" | ConvertTo-Json -Depth 5
```

Expected health output:
- `status: ok`
- `mongodb: connected`
- `redis: connected`

## Common Issues
### Docker permission error in Jenkins
- Jenkins service account cannot access Docker.
- Fix by running Jenkins under a user with Docker access.

### Port 1000 already in use
- Stop conflicting service/container or change Jenkins pipeline app port.

### Health check fails
- Incorrect Mongo/Redis environment values.
- Check build logs and container logs:

```powershell
docker logs --tail 100 incident-platform-ci
```

## Why Pipeline over Freestyle
- Pipeline is code (`Jenkinsfile`) and version controlled.
- Easier for team collaboration and audits.
- Reproducible CI/CD behavior across environments.
