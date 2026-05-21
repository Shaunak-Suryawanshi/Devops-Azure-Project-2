# Monitoring Setup Runbook (Step 12)

This runbook documents Prometheus and Grafana setup on Minikube.

## Files Used
- `infra/monitoring/prometheus-configmap.yaml`
- `infra/monitoring/prometheus.yaml`
- `infra/monitoring/grafana-datasource-configmap.yaml`
- `infra/monitoring/grafana.yaml`

## Prerequisites
- Step 11 Kubernetes app is already running in namespace `incident-platform`.
- App exposes `/metrics` endpoint.

## Apply Monitoring Manifests

```powershell
kubectl apply -f infra/monitoring/prometheus-configmap.yaml
kubectl apply -f infra/monitoring/prometheus.yaml
kubectl apply -f infra/monitoring/grafana-datasource-configmap.yaml
kubectl apply -f infra/monitoring/grafana.yaml
```

## Verify Pods

```powershell
kubectl get pods -n incident-platform -w
```

Expected:
- `prometheus` pod -> `Running`
- `grafana` pod -> `Running`

## Access Prometheus and Grafana

```powershell
minikube service prometheus -n incident-platform --url
minikube service grafana -n incident-platform --url
```

Grafana login defaults:
- user: `admin`
- password: `admin`

## Datasource
Prometheus datasource is auto-provisioned using ConfigMap:
- URL: `http://prometheus:9090`
- Set as default datasource.

## Quick Metric Check
In Grafana Explore, run query:
- `flask_http_request_total`

If results appear, app metrics scraping is working.

## Troubleshooting
### Prometheus pod not starting
- Check config map exists and mount path is correct.
- Run:

```powershell
kubectl logs deployment/prometheus -n incident-platform
```

### Grafana shows no data
- Ensure app `/metrics` endpoint is reachable by Prometheus.
- Check Prometheus targets UI (`Status -> Targets`) shows `incident-app:1000` as `UP`.

### Service URL not opening
- Ensure Minikube is running.
- Use `minikube service <name> -n incident-platform --url`.

## Interview Talking Points
- Added application-level metrics with Prometheus exporter.
- Used Prometheus ConfigMap for scrape configuration.
- Used Grafana provisioning ConfigMap for zero-click datasource setup.
- Exposed monitoring tools via NodePort services for local cluster access.
