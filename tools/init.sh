#!/bin/bash
echo "Initializing JR Journal Environment..."
gcloud config set project jr-journal-app
source .venv/bin/activate
export PROJECT_ID=$(gcloud config get-value project)
export SA_EMAIL=$(gcloud iam service-accounts list --filter="email:jr-journal-service*" --format="value(email)")
echo "Environment set! Project: $PROJECT_ID | SA: $SA_EMAIL"
