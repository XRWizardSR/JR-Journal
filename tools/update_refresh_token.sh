#!/bin/bash

# This script extracts the refresh token from 'token.json' and uploads it to Secret Manager.

# 1. Check for token.json
if [ ! -f "token.json" ]; then
    echo "❌ ERROR: 'token.json' not found."
    echo "Please run './tools/run_local.sh' and complete the Google Calendar authentication first."
    exit 1
fi

# 2. Check for jq
if ! command -v jq &> /dev/null
then
    echo "❌ ERROR: 'jq' is not installed. Please install it to proceed."
    echo "On Debian/Ubuntu: sudo apt-get install jq"
    echo "On macOS: brew install jq"
    exit 1
fi

echo "🔐 Extracting refresh token from 'token.json'..."
REFRESH_TOKEN=$(jq -r .refresh_token token.json)

if [ -z "$REFRESH_TOKEN" ] || [ "$REFRESH_TOKEN" == "null" ]; then
    echo "❌ ERROR: Could not find a refresh_token in 'token.json'."
    echo "Please ensure you have authenticated correctly."
    exit 1
fi

echo "🔐 Uploading refresh token to Secret Manager..."
# The -n flag for echo prevents adding a trailing newline
echo -n "$REFRESH_TOKEN" | gcloud secrets versions add google-refresh-token --data-file=- --quiet

echo "✅ Refresh token successfully updated in Secret Manager!"
echo "You are now ready to deploy the agent."
