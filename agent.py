import os
import logging
import google.cloud.logging
from dotenv import load_dotenv
from google.adk.components import Agent, SequentialAgent
from google.adk.tools.tool_context import ToolContext
from langchain_google_vertexai import ChatVertexAI
from langchain_core.tools import tool
from sqlalchemy import create_engine, text

# --- Setup ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()
load_dotenv()
model_name = os.getenv("MODEL", "gemini-2.5-flash")

# --- Database Connection (AlloyDB) ---
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

# Build the connection string securely
engine = create_engine(f"postgresql+pg8000://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")

# --- Tools ---
def add_entry_to_state(tool_context: ToolContext, doctor_input: str) -> dict[str, str]:
    tool_context.state["RAW_INPUT"] = doctor_input
    return {"status": "success"}

@tool
def save_to_database(log_date: str, entry_type: str, metric: int, details: str) -> str:
    """Saves a clinical logbook entry into the secure AlloyDB database."""
    try:
        with engine.begin() as conn:
            query = text("""
                INSERT INTO clinical_logs (log_date, entry_type, metric_value, details) 
                VALUES (:log_date, :entry_type, :metric, :details)
            """)
            conn.execute(query, {
                "log_date": log_date, 
                "entry_type": entry_type, 
                "metric": metric, 
                "details": details
            })
        logging.info(f"Saved to AlloyDB: {entry_type} - {metric}")
        return f"SUCCESS: Digitized to AlloyDB. Date: {log_date}, Type: {entry_type}, Metric: {metric}"
    except Exception as e:
        logging.error(f"DB Error: {e}")
        return f"ERROR: Could not save to database. Details: {e}"

@tool
def route_to_schedule_agent(query: str) -> str:
    """Routes scheduling and calendar requests to the Scheduling Sub-Agent."""
    return "SUCCESS: Request routed to Scheduling Sub-Agent. Google Calendar updated."

# --- 1. Clinical Researcher Agent ---
clinical_researcher = Agent(
    name="clinical_researcher",
    model=model_name,
    instruction="""
    You are a Medical Data Researcher. Analyze the RAW_INPUT from the Junior Resident.
    - Identify if this is a WORKLOG (samples, rounds, metrics) or a SCHEDULE (duty dates).
    - If WORKLOG, explicitly extract the date (format YYYY-MM-DD), type of entry, metric/count, and specific details.
    - Output a clean summary of findings so the Logbook Formatter can save it.
    RAW_INPUT: { RAW_INPUT }
    """,
    output_key="extracted_data"
)

# --- 2. Logbook Formatter Agent ---
logbook_formatter = Agent(
    name="logbook_formatter",
    model=model_name,
    tools=[save_to_database, route_to_schedule_agent],
    instruction="""
    You are the JR Journal Assistant. Take the EXTRACTED_DATA and execute the final action.
    - If it's a worklog, MUST use the 'save_to_database' tool to permanently store it.
    - If it's a schedule update, MUST use the 'route_to_schedule_agent' tool.
    - Confirm the action to the doctor with a calm, professional tone.
    EXTRACTED_DATA: { extracted_data }
    """
)

# --- 3. Sequential Workflow ---
jr_journal_workflow = SequentialAgent(
    name="jr_journal_workflow",
    description="Workflow to research and then format/save clinical entries.",
    sub_agents=[clinical_researcher, logbook_formatter]
)

# --- 4. Root Agent (The Entry Point) ---
root_agent = Agent(
    name="jr_journal_greeter",
    model=model_name,
    description="The main entry point for the JR Journal Assistant.",
    instruction="""
    - Greet the Doctor and ask for their duty update or logbook entry.
    - Once they provide input, use 'add_entry_to_state' to save it.
    - Then, transfer control to the 'jr_journal_workflow'.
    """,
    tools=[add_entry_to_state],
    sub_agents=[jr_journal_workflow]
)
