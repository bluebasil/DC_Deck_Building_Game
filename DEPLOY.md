# DC Deck Builder — Deployment Guide

## Architecture

```
[S3 Static Website]
        ↕  WebSocket / HTTP
[Cloud Run — Flask + game thread]
   - Scales to 0 when idle  →  ~$0/month at rest
   - WebSocket support via gevent
   - Game state in-memory (one game per container)
```

## Prerequisites

1. **GCP project** — enable these APIs:
   ```
   gcloud services enable run.googleapis.com \
     artifactregistry.googleapis.com \
     --project=YOUR_PROJECT_ID
   ```
2. **Docker** installed locally
3. **Terraform >= 1.5** installed
4. **gcloud CLI** authenticated: `gcloud auth login`
5. Configure Docker for Artifact Registry:
   ```
   gcloud auth configure-docker REGION-docker.pkg.dev
   ```

---

## One-time Setup (Terraform)

```bash
cd terraform

# Create terraform.tfvars
cat > terraform.tfvars <<EOF
project_id = "your-gcp-project-id"
region     = "us-central1"
EOF

terraform init
terraform apply
```

This creates:
- Artifact Registry repository
- Cloud Run service (min 0, max 1 instance)
- Public IAM binding

---

## Deploy (build & push)

Run from the project root each time you want to update:

```bash
# Set your values
PROJECT_ID="your-gcp-project-id"
REGION="us-central1"
SERVICE="dc-deck-builder"
IMAGE="${REGION}-docker.pkg.dev/${PROJECT_ID}/${SERVICE}/${SERVICE}"
TAG=$(git rev-parse --short HEAD 2>/dev/null || echo "latest")

# Build
docker build -t "${IMAGE}:${TAG}" -t "${IMAGE}:latest" .

# Push
docker push "${IMAGE}:${TAG}"
docker push "${IMAGE}:latest"

# Update Cloud Run (or let Terraform handle it)
gcloud run deploy ${SERVICE} \
  --image "${IMAGE}:${TAG}" \
  --region ${REGION} \
  --project ${PROJECT_ID}
```

---

## Frontend (S3)

The `frontend/` folder is served directly by the Flask backend. For the **standalone S3 website** you already have, update `game.js` line 7:

```javascript
const SERVER_URL = 'https://YOUR-CLOUD-RUN-URL.run.app';
```

Then copy the frontend files to S3:
```bash
aws s3 sync frontend/ s3://your-bucket-name/ --delete
```

The Cloud Run service already has `cors_allowed_origins="*"` so cross-origin requests from S3 will work.

---

## Local Development

```bash
# Install dependencies (no arcade needed for web mode)
pip install -r requirements.txt

# Run locally
python web_server.py

# Open browser at http://localhost:8080
```

To test with arcade too (original game):
```bash
pip install arcade
python main.py
```

---

## Cost Estimate

| Scenario | Cost |
|---|---|
| Idle (no games running) | **$0** (scales to zero) |
| 1 hour of play/day | ~$0.01–0.03 |
| Playing all day every day | ~$0.50–2.00 |

Cloud Run free tier: 180,000 vCPU-seconds + 360,000 GB-seconds per month.
A 1-hour game uses roughly 3,600 vCPU-seconds → ~50 free hours/month.

---

## Troubleshooting

**WebSocket not connecting:**
- Cloud Run supports WebSockets natively; check that `session-affinity` isn't needed (it shouldn't be for single-instance)
- Check CORS: the S3 URL must be reachable from the frontend

**`arcade` import errors on Cloud Run:**
- The code conditionally imports arcade — it's not required for the web server
- Make sure `arcade` is NOT in `requirements.txt` (it isn't)

**Cold start delay (~2–4 s):**
- Expected with scale-to-zero; the first request after idle takes a few seconds
- The frontend shows "Connecting…" while this happens

**Game stuck after starting:**
- Check Cloud Run logs: `gcloud run logs read --service=dc-deck-builder --region=us-central1`
- The game thread logs to stdout which appears in Cloud Run logs
