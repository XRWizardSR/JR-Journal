# 🏗 Technical Architecture

JR Journal utilizes a highly modular, serverless architecture on Google Cloud, designed for high availability and data security.

## System Flow

1. **User Access & Input:** The Junior Resident provides natural language input (Voice/Text) via the frontend interface.
2. **API Gateway & Auth:** Traffic is routed through Google Cloud Identity Platform to ensure secure, authenticated access.
3. **Core Agent Orchestration (Cloud Run):**
   The request hits the **Chief Resident Agent** (powered by Vertex AI Gemini Models and the ADK framework). 
   * It analyzes the intent and dispatches tools.
4. **Tool & Data Integration (MCP):**
   The system uses the Model Context Protocol (MCP) to standardize connections to external systems.
   * **Path A (Scheduling):** The Scheduling Sub-Agent uses the Google Calendar API to sync duty rosters (Academic/Cultural/Night Dates).
   * **Path B (Logbook):** The Logbook Sub-Agent uses AlloyDB for PostgreSQL to persist clinical records (Sample Counts, HIC Rounds, Worklogs).
5. **Feedback Loop:**
   The Chief Resident Agent consolidates the actions from the sub-agents and provides a success summary back to the user (e.g., *"Logbook updated. Shift added to calendar."*).

## Management & Monitoring
The entire containerized application is monitored using:
* **Cloud Logging:** For tracking agent execution and tool dispatching.
* **Cloud Monitoring:** For performance and uptime tracking.
* **Secret Manager:** For securing database credentials and API keys.