#!/bin/bash
echo "🚀 Starting JR Journal Agent locally..."
echo "If this is your first time, a browser window will open for Google Calendar authentication."

# The 'adk run' command starts a local server for the agent.
uvx --from google-adk==1.14.0 adk run .
