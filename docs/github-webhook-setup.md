# GitHub Webhook Setup with ngrok (Step 9)

This runbook enables automatic Jenkins pipeline trigger when code is pushed to GitHub.

## Goal
GitHub push -> Webhook call -> Jenkins pipeline starts automatically.

## Prerequisites
- Jenkins pipeline job is already working manually.
- Jenkins job is configured with:
  - `Pipeline script from SCM`
  - Script path: `infra/jenkins/Jenkinsfile`
- ngrok installed.

## 1) Start ngrok tunnel

```powershell
ngrok http 8080
```

Copy HTTPS forwarding URL, for example:
- `https://abcd-1234.ngrok-free.app`

## 2) Configure Jenkins job trigger
In Jenkins job -> Configure:
- Enable `GitHub hook trigger for GITScm polling`
- Save.

## 3) Configure GitHub webhook
In GitHub repo:
- Settings -> Webhooks -> Add webhook

Set:
- Payload URL: `https://<ngrok-url>/github-webhook/`
- Content type: `application/json`
- Events: `Just the push event`
- Active: checked

## 4) Validate
Push any commit (or empty commit):

```powershell
git commit --allow-empty -m "test: webhook trigger"
git push origin main
```

Expected:
- GitHub delivery status is `200`
- Jenkins build starts with message similar to `Started by GitHub push...`

## 5) Troubleshooting
### Jenkins not triggered
- Check webhook URL path includes `/github-webhook/`
- Check Jenkins job trigger option is enabled
- Ensure ngrok is still running

### GitHub delivery failed
- Open webhook -> Recent Deliveries -> inspect response code/body

### Wrong branch trigger
- In Jenkins SCM branch specifier use `*/main`

## Security Notes
- Do not store cloud passwords in repo files.
- Use Jenkins Credentials for secrets.
- Rotate any secret that was accidentally exposed.
