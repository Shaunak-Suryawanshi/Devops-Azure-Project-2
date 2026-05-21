# Kubernetes on Minikube Runbook (Step 11 + Step 13)

This runbook documents deployment and advanced operations for the 3-tier platform on Minikube.

## Files Used
- `infra/k8s/namespace.yaml`
- `infra/k8s/mongo.yaml`
- `infra/k8s/redis.yaml`
- `infra/k8s/app.yaml`
- `infra/k8s/app-configmap.yaml`
- `infra/k8s/app-secret.yaml`

## Initial Apply (Step 11)

```powershell
kubectl apply -f infra/k8s/namespace.yaml
kubectl apply -f infra/k8s/mongo.yaml
kubectl apply -f infra/k8s/redis.yaml
kubectl apply -f infra/k8s/app.yaml
```

## Advanced Apply (Step 13)

```powershell
kubectl apply -f infra/k8s/app-configmap.yaml
kubectl apply -f infra/k8s/app-secret.yaml
kubectl apply -f infra/k8s/app.yaml
```

## What Step 13 Adds
- Replicas: app scaled to 2
- Rolling strategy:
  - `maxSurge: 1`
  - `maxUnavailable: 0`
- Health probes:
  - readiness: `/health`
  - liveness: `/health`
- Externalized config:
  - ConfigMap for non-secret values
  - Secret for sensitive values

## Verify Rollout

```powershell
kubectl rollout status deployment/incident-app -n incident-platform
kubectl get deploy -n incident-platform
kubectl get pods -n incident-platform -w
```

Expected:
- `incident-app` shows `2/2` available
- both app pods `Running` and `Ready`

## Access Application

```powershell
minikube service incident-app -n incident-platform --url
```

## Common Issue: ImagePullBackOff
If using local image only:

```powershell
minikube image load incident-platform:latest
kubectl rollout restart deployment/incident-app -n incident-platform
```

## Interview Talking Points
- Used rolling updates to reduce downtime risk.
- Added readiness/liveness probes for safer self-healing.
- Moved config to ConfigMap and secrets to Secret for production-style separation.
- Scaled app tier horizontally from 1 to 2 replicas.

## Cleanup

```powershell
kubectl delete namespace incident-platform
```
