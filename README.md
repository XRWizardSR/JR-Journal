# 🩺 JR Journal: Digital Sanctuary for Medical Residents

**JR Journal** is an AI-powered, multi-agent productivity assistant built for the **GenAI Academy APAC Hackathon 2026**. It is specifically designed to eliminate administrative burnout for medical Junior Residents (JRs), with an initial focus on MD Microbiology workflows.

## 🚀 The Clinical Problem
Medical residents suffer from severe administrative burnout. During grueling 24-hour shifts, they are forced to manually track complex, overlapping schedules (Night shifts, Weekend duties, Academic rosters) and maintain physical logbooks of hundreds of daily clinical procedures (e.g., logging sample testing volumes, HIC rounds). 

## 💡 Our Solution & USP
**Unique Selling Proposition (USP): "Voice-to-Logbook Integration."**
A doctor can simply dictate their daily metrics or schedule updates in natural language after a long shift (e.g., *"I tested 750 blood samples today and have night duty tomorrow"*). The multi-agent system autonomously categorizes, structures, and logs the data into secure databases and calendars without a single manual form entry.

## 🧠 Multi-Agent Orchestration (How it Works)
Built using the Google Agent Development Kit (ADK), JR Journal utilizes a "Chief Resident" primary agent that orchestrates specialized sub-agents:

1. **Chief Resident Agent (Primary):** Analyzes intent, extracts key data, and coordinates sub-agents.
2. **Logbook Agent (Sub-Agent):** Structures clinical data (e.g., "750 samples tested") and securely persists it to Google AlloyDB via MCP.
3. **Scheduling Agent (Sub-Agent):** Identifies date/duty types and syncs events to Google Calendar via MCP.

## 🛠 Tech Stack
* **Framework:** Google Agent Development Kit (ADK)
* **Brain:** Vertex AI (Gemini Models)
* **Integration:** Model Context Protocol (MCP) Tool Connectors
* **Database:** Google AlloyDB for PostgreSQL (Structured Clinical Logs)
* **Infrastructure:** Google Cloud Run (Serverless Container API)

*Why this stack?* Serverless deployment (Cloud Run) ensures cost-effective scaling and high availability during unpredictable hospital shifts, while AlloyDB provides the transactional reliability required for medical data.

## 🚀 End-to-End Deployment Guide

This guide provides the full workflow for setting up, testing, and deploying the JR Journal agent, including secure secret management.

### Step 1: Initial Setup
First, initialize your local environment. This script sets your gcloud project, activates the virtual environment, and exports necessary environment variables.
```bash
source tools/init.sh
```

### Step 2: Set Up Google Cloud Secrets
This step securely stores your application credentials in Google Cloud Secret Manager.

**Prerequisite:** Make sure you have downloaded your OAuth 2.0 Client ID as `credentials.json` and placed it in the root of this project.

Run the setup script:
```bash
bash tools/setup_secrets.sh
```

### Step 3: Local Run & Authentication
Run the agent locally to perform the one-time Google Calendar authentication. This will open a browser window for you to grant permission.
```bash
bash tools/run_local.sh
```
After you approve, a `token.json` file will be created in your project directory.

### Step 4: Upload the Refresh Token
The `token.json` contains a vital `refresh_token` that the deployed agent will use. Run the following script to extract this token and upload it securely to Secret Manager.
```bash
bash tools/update_refresh_token.sh
```

### Step 5: Deploy to Cloud Run
With your secrets securely stored, you can now deploy the agent to Cloud Run. It will use the secrets to run headlessly without any further manual login.
```bash
bash tools/deploy.sh
```

## 🏗 Architecture Notes & MCP Compatibility (Phase 2)
To deliver a secure, database-backed MVP within the 24-hour hackathon constraint, we proved the core multi-agent logic, data extraction, and secure VPC database persistence using native ADK tools. 

Our architecture is designed to decouple these tools into a standalone **Model Context Protocol (MCP)** server (`mcp_server.py`) and connect to our custom "Clinical Ethereal" frontend (`/ui`) in Phase 2, ensuring enterprise scalability while fulfilling all hackathon MCP requirements.