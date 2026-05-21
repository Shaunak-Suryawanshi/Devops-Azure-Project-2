# Kubernetes on Minikube Runbook (Step 11)

This runbook documents deployment of the 3-tier incident platform on Minikube.

## Files Used
- `infra/k8s/namespace.yaml`
- `infra/k8s/mongo.yaml`
- `infra/k8s/redis.yaml`
- `infra/k8s/app.yaml`

## Apply Order

```powershell
kubectl apply -f infra/k8s/namespace.yaml
kubectl apply -f infra/k8s/mongo.yaml
kubectl apply -f infra/k8s/redis.yaml
kubectl apply -f infra/k8s/app.yaml
```

## Verify Resources

```powershell
kubectl get all -n incident-platform
kubectl get pods -n incident-platform -w
```

Expected:
- `mongo` pod: `Running`
- `redis` pod: `Running`
- `incident-app` pod: `Running`

## Common Issue: App ImagePullBackOff
If app image is local only, Minikube cannot pull it from Docker Hub by default.

Fix:

```powershell
minikube image load incident-platform:latest
kubectl rollout restart deployment/incident-app -n incident-platform
kubectl get pods -n incident-platform -w
```

## Access Application

```powershell
minikube service incident-app -n incident-platform --url
```

Open URL and test:
- `/`
- `/health`

## Why Services Work by Name
In Kubernetes, app connects to:
- Mongo service DNS: `mongo`
- Redis service DNS: `redis`

This keeps app config stable even when pod IPs change.

## Interview Talking Points
- Used `Namespace` for workload isolation.
- Used `Deployment` for each tier (self-healing, rollout support).
- Used `ClusterIP` services for internal DB/cache.
- Used `NodePort` service for external app access in Minikube.
- Handled local image pull issue with `minikube image load`.

## Cleanup

```powershell
kubectl delete namespace incident-platform
```
