QR Management Web App — Docker Deployment Handbook
1. Make code changes

Make and test your changes in VS Code.

2. Run tests
pytest

If tests pass, continue.

3. Check Git changes
git status
git diff
4. Build Docker image locally

From the project root:

docker build -t qr-scanner-web .
5. Test the Docker image locally
docker run --rm -p 8080:8080 qr-scanner-web

Open:

http://localhost:8080

Stop the container with Ctrl+C.

6. Configure Google Cloud

Set the project:

gcloud config set project qr-scanner-web-505819

Set the region:

gcloud config set run/region europe-west1
7. Build and push the image to Artifact Registry

If your repository is:

europe-west1-docker.pkg.dev/qr-scanner-web-505819/qr-scanner-web

build:

docker build -t europe-west1-docker.pkg.dev/qr-scanner-web-505819/qr-scanner-web:latest .

Push:

docker push europe-west1-docker.pkg.dev/qr-scanner-web-505819/qr-scanner-web:latest
8. Deploy to Cloud Run
gcloud run deploy qr-scanner-web `
  --image europe-west1-docker.pkg.dev/qr-scanner-web-505819/qr-scanner-web:latest `
  --region europe-west1 `
  --platform managed
9. Important printer configuration

For the Cloud Run web application, make sure the environment variables are:

PRINTER_ENABLED=true
PRINT_AGENT_URL=http://127.0.0.1:8765

You can configure them during deployment with:

gcloud run deploy qr-scanner-web `
  --image europe-west1-docker.pkg.dev/qr-scanner-web-505819/qr-scanner-web:latest `
  --region europe-west1 `
  --set-env-vars="PRINTER_ENABLED=true,PRINT_AGENT_URL=http://127.0.0.1:8765"

Be careful: --set-env-vars can replace/update environment variables, so for your production deployment I'd prefer maintaining the complete required environment configuration in Cloud Run rather than accidentally dropping existing variables.

10. Verify deployment

Get the service URL:

gcloud run services describe qr-scanner-web `
  --region europe-west1 `
  --format="value(status.url)"

Open the URL.

Then test the local Print Agent from the browser console:

fetch("http://127.0.0.1:8765/health")
  .then(r => r.json())
  .then(console.log)
  .catch(console.error);

Expected:

{
  agent: "online",
  printer: "Zebra ZD230 printer",
  printer_available: true
}
11. Final application test
✓ Login
✓ Dashboard
✓ Generate QR
✓ QR printing
✓ Print History
✓ Reprint
✓ Partial/Pending reprint
✓ Printer Connected status
✓ Printer OFF status
✓ Print Agent stopped status
12. Git workflow

After everything is verified:

git add .
git commit -m "Describe the change"
git push origin main

If your Cloud Build trigger is configured to build the Docker image and deploy Cloud Run automatically, this becomes your normal production flow:

VS Code
   ↓
pytest
   ↓
git commit
   ↓
git push
   ↓
GitHub
   ↓
Cloud Build
   ↓
Docker build
   ↓
Artifact Registry
   ↓
Cloud Run
   ↓
QR Management Web App
   ↓
Browser → Windows Print Agent → Zebra

One correction to my previous answer: if you're using the existing Cloud Build trigger, you generally don't need to manually docker push or gcloud run deploy for every code change. Those commands are useful for a manual deployment/troubleshooting procedure; your normal handbook can use the Git push flow.