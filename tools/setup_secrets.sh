#!/bin/bash

# This script sets up the necessary Google Cloud Secrets for the JR Journal agent.

# 1. Check for credentials.json
if [ ! -f "credentials.json" ]; then
    echo "❌ ERROR: 'credentials.json' not found."
    echo "Please download your OAuth 2.0 Client ID for a 'Desktop app' from the Google Cloud Console and place it in the root directory."
    exit 1
fi

echo "🔐 Enabling Secret Manager API..."
gcloud services enable secretmanager.googleapis.com

# 2. Create and populate the credentials secret
echo "🔐 Creating secret 'google-credentials-json'..."
gcloud secrets create google-credentials-json --replication-policy="automatic" --quiet || echo "Secret 'google-credentials-json' already exists. Skipping creation."

echo "🔐 Uploading 'credentials.json' to Secret Manager..."
gcloud secrets versions add google-credentials-json --data-file="credentials.json" --quiet

# 3. Create a placeholder for the refresh token
echo "🔐 Creating secret 'google-refresh-token'..."
gcloud secrets create google-refresh-token --replication-policy="automatic" --quiet || echo "Secret 'google-refresh-token' already exists. Skipping creation."
echo "An empty refresh token secret has been created. It will be populated after you run the agent locally for the first time."

# 4. Grant Service Account access to the secrets
echo "🔐 Granting Service Account '$SA_EMAIL' access to secrets..."
gcloud secrets add-iam-policy-binding google-credentials-json 
  --member="serviceAccount:$SA_EMAIL" 
  --role="roles/secretmanager.secretAccessor" --quiet

gcloud secrets add-iam-policy-binding google-refresh-token 
  --member="serviceAccount:$SA_EMAIL" 
  --role="roles/secretmanager.secretAccessor" --quiet

echo "✅ Secret setup complete!"
echo "You are now ready to run the agent locally to generate your refresh token."
