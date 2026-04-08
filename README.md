# JR Journal: The Digital Sanctuary for AIIMS Residents

**JR Journal** is a multi-agent AI system built for the GenAI Academy APAC Hackathon. It is designed to solve administrative burnout for Junior Residents (specifically targeting MD Microbiology workflows).

## 🚀 Problem Statement
Medical residents manage grueling 24-hour shifts while being required to manually track clinical worklogs (thousands of samples) and complex duty rosters (Academic, Cultural, Night, Weekend).

## 🛠 Features & Multi-Agent Workflow
- **Chief Resident (Primary Agent):** Acts as the central orchestrator using Gemini 2.5 Flash to route requests.
- **Logbook Agent (Tool):** Uses MCP to extract metrics from natural language and store structured data in AlloyDB.
- **Schedule Agent (Tool):** Manages duty rosters via Google Calendar integration.

## 🏗 Tech Stack
- **AI Framework:** Google ADK (Agent Development Kit)
- **Model:** Gemini 2.5 Flash (via Vertex AI)
- **Infrastructure:** Google Cloud Run
- **Database:** AlloyDB (Structured Clinical Logs)
- **Integration:** Model Context Protocol (MCP)
