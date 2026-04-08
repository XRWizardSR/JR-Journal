#!/bin/bash
echo "Deploying JR Journal Agent to Cloud Run..."
uvx --from google-adk==1.14.0 \
adk deploy cloud_run \
  --project=$PROJECT_ID \
  --region=us-central1 \
  --service_name=jr-journal-agent \
  --with_ui \
  . \
  -- \
  --service-account=$SA_EMAIL \
  --allow-unauthenticated \
  --network=default \
  --vpc-egress=private-ranges-only \
  --set-env-vars="DB_USER=postgres,DB_PASS=AishuRajesh,DB_HOST=10.80.128.2,DB_NAME=jr_journal_db,PROJECT_ID=$PROJECT_ID"
