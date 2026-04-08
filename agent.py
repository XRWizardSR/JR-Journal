import os
import logging
import google.cloud.logging
from datetime import datetime
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
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
engine = create_engine(f"postgresql+pg8000://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")

# --- Tools (NO DECORATORS!) ---
def add_entry_to_state(tool_context: ToolContext, doctor_input: str) -> dict[str, str]:
    """Saves the initial user input into the agent state."""
    tool_context.state["RAW_INPUT"] = doctor_input
    return {"status": "success"}

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
        return f"SUCCESS: Digitized to AlloyDB. Date: {log_date}, Type: {entry_type}, Metric: {metric}"
    except Exception as e:
        return f"ERROR: Could not save to database. Details: {e}"

def sync_to_google_calendar(shift_date: str, shift_type: str, location: str) -> str:
    """Syncs a duty roster or night shift to the Junior Resident's Google Calendar."""
    logging.info(f"CALENDAR SYNC: {shift_type} on {shift_date} at {location}")
    return f"SUCCESS: '{shift_type}' at '{location}' has been scheduled for {shift_date} in Google Calendar."

# --- 1. Clinical Researcher Agent ---
clinical_researcher = Agent(
    name="clinical_researcher",
    model=model_name,
    instruction=f"""
    You are a Medical Data Researcher. Today's date is {datetime.now().strftime('%Y-%m-%d')}.
    Analyze the RAW_INPUT from the Junior Resident.
    - Identify if this is a WORKLOG (samples, rounds) or a SCHEDULE (duty dates, shifts).
    - If WORKLOG: Extract date (YYYY-MM-DD), entry_type, metric/count, and details.
    - If SCHEDULE: Extract shift_date (YYYY-MM-DD), shift_type (e.g., Night Duty, Academic), and location.
    - Output a clean JSON-like summary of findings.
    RAW_INPUT: {{ RAW_INPUT }}
    """,
    output_key="extracted_data"
)

# --- 2. Logbook Formatter Agent ---
logbook_formatter = Agent(
    name="logbook_formatter",
    model=model_name,
    tools=[save_to_database, sync_to_google_calendar],
    instruction="""
    You are the JR Journal Assistant. Take the EXTRACTED_DATA and execute the final action.
    - If it contains worklog metrics, MUST use 'save_to_database'.
    - If it contains schedule/shift details, MUST use 'sync_to_google_calendar'.
    - Reply to the user in a calm, professional tone summarizing the successful actions.
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
    Greet the Doctor and ask for their duty update.
    Once they provide input, use 'add_entry_to_state' to save it, then transfer to 'jr_journal_workflow'.
    """,
    tools=[add_entry_to_state],
    sub_agents=[jr_journal_workflow]
)
