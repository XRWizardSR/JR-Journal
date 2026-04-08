# 🏗 Technical Architecture

JR Journal utilizes a highly modular, serverless architecture on Google Cloud, designed for high availability and data security.

## System Flow (MVP)

1. **User Access & Input:** The Junior Resident provides natural language input (Voice/Text) via the frontend interface.
2. **API Gateway & Auth:** Traffic is securely routed to the Cloud Run service, utilizing a dedicated Service Account (`jr-journal-service`) with minimum required IAM permissions (`roles/aiplatform.user`, `roles/alloydb.client`).
3. **Core Agent Orchestration (Cloud Run):**
   The request is processed by a **Sequential Multi-Agent System** built on the Google Agent Development Kit (ADK).
   * **Primary Agent (Greeter):** Captures the initial user state and transfers control.
   * **Sub-Agent 1 (Clinical Researcher):** Analyzes intent and extracts structured data (Date, Metric, Type) from medical natural language.
   * **Sub-Agent 2 (Logbook Formatter):** Routes the extracted data to the appropriate tool and formats a professional response.
4. **Tool & Data Integration:**
   * **Path A (Scheduling):** The system identifies duty roster updates and dispatches the `sync_to_google_calendar` tool.
   * **Path B (Logbook):** The system utilizes **Google AlloyDB for PostgreSQL** for secure, structured data persistence. Connection is established over a private VPC Peering tunnel using SQLAlchemy and the `pg8000` driver.
5. **Feedback Loop:**
   The agents consolidate actions and provide a success summary back to the user (e.g., *"Digitized to AlloyDB. Metric: 1000"*).

## Phase 2: MCP & Frontend Decoupling

To ensure enterprise scalability, the architecture is designed for immediate transition to a decoupled state:
* **Frontend:** A high-fidelity interface ("Clinical Ethereal") served via FastAPI, interacting with the backend agents through standardized API endpoints.
* **MCP Server:** Tools are migrated to a standalone **Model Context Protocol (MCP)** server (`mcp_server.py`). This allows the agents to dynamically discover and consume tools like `save_clinical_log` and `retrieve_clinical_logs` via the MCP standard.

## Management & Monitoring
The entire containerized application is monitored using:
* **Cloud Logging:** Tracks agent execution, state transitions, and tool dispatching.
* **Cloud Monitoring:** Monitors performance, latency, and uptime.
* **VPC Network:** Ensures all database traffic remains on the private Google backbone, isolated from the public internet.