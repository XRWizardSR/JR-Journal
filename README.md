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

## 🚀 Quick Start & Deployment

We have automated the environment initialization and Cloud Run deployment to ensure a reproducible build process.

1. **Initialize the Environment:**
   `source tools/init.sh`

2. **Deploy to Google Cloud Run:**
   `./tools/deploy.sh`

## 🏗 Architecture Notes & MCP Compatibility (Phase 2)
To deliver a secure, database-backed MVP within the 24-hour hackathon constraint, we proved the core multi-agent logic, data extraction, and secure VPC database persistence using native ADK tools. 

Our architecture is designed to decouple these tools into a standalone **Model Context Protocol (MCP)** server (`mcp_server.py`) and connect to our custom "Clinical Ethereal" frontend (`/ui`) in Phase 2, ensuring enterprise scalability while fulfilling all hackathon MCP requirements.