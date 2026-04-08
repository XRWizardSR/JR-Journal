# 🩺 JR Journal: The Digital Sanctuary for AIIMS Residents

**JR Journal** is a sophisticated multi-agent AI system built for the **GenAI Academy APAC Hackathon 2026**. It transforms the high-friction administrative overhead of Junior Residents (JRs) into a seamless, digital experience.

## 🚀 The Clinical Problem
In high-intensity environments like **MD Microbiology**, residents are buried under manual logs. Tracking thousands of blood samples or HIC rounds while managing 24-hour duty rosters leads to burnout and data entry errors.

## 🧠 Multi-Agent Orchestration & Workflow
Unlike a basic chatbot, **JR Journal** utilizes a **Sequential Workflow** to ensure data integrity and professional formatting:

* **Greeter (Primary Agent):** The central entry point that captures the doctor's unstructured input and manages the global state.
* **Clinical Researcher (Sub-Agent 1):** Extracts structured metrics (sample counts, duty types, dates) from natural language.
* **Response Formatter (Sub-Agent 2):** Synthesizes the data into a professional confirmation and prepares the logs for the database.

## 🛠 Tech Stack & Infrastructure
* **Orchestration:** Google Agent Development Kit (ADK) `v1.14.0`.
* **Brain:** Gemini 2.5 Flash via **Vertex AI** (authenticated via IAM Service Accounts).
* **Deployment:** Google **Cloud Run** with an auto-generated **ADK UI**.
* **Tools:** Custom Python tools for **AlloyDB** (Clinical Logs) and Google Calendar (Rosters).

## 📦 Local Setup & Deployment
1.  **Environment:** `uv venv && source .venv/bin/activate`.
2.  **Identity:** Managed via a dedicated `jr-journal-service` account with `aiplatform.user` permissions.
3.  **Deploy:** `uvx --from google-adk adk deploy cloud_run --with_ui`.
