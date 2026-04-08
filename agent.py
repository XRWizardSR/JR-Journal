import os
import json
import logging
import google.cloud.logging
from datetime import datetime, timedelta
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from sqlalchemy import create_engine, text

# --- Google API Imports ---
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google.cloud import secretmanager

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

# --- Google Calendar Auth ---
SCOPES = ["https://www.googleapis.com/auth/calendar.events"]

def get_calendar_service():
    """Gets an authorized Google Calendar service object, handling both local and Cloud Run environments."""
    creds = None
    
    # Check if running in Cloud Run
    if "K_SERVICE" in os.environ:
        project_id = os.getenv("PROJECT_ID")
        sm_client = secretmanager.SecretManagerServiceClient()
        
        # Get credentials from Secret Manager
        cred_secret_name = f"projects/{project_id}/secrets/google-credentials-json/versions/latest"
        cred_response = sm_client.access_secret_version(request={"name": cred_secret_name})
        cred_info = json.loads(cred_response.payload.data.decode("UTF-8"))

        # Get refresh token from Secret Manager
        token_secret_name = f"projects/{project_id}/secrets/google-refresh-token/versions/latest"
        token_response = sm_client.access_secret_version(request={"name": token_secret_name})
        refresh_token = token_response.payload.data.decode("UTF-8")
        
        creds = Credentials(
            None, # No access token initially
            refresh_token=refresh_token,
            token_uri=cred_info['installed']['token_uri'],
            client_id=cred_info['installed']['client_id'],
            client_secret=cred_info['installed']['client_secret'],
            scopes=SCOPES
        )
        creds.refresh(Request())
    else:
        # Local development flow
        if os.path.exists("token.json"):
            creds = Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())

    return build("calendar", "v3", credentials=creds)

# --- Tools ---
def add_entry_to_state(tool_context: ToolContext, doctor_input: str) -> dict[str, str]:
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
                "log_date": log_date, "entry_type": entry_type, "metric": metric, "details": details
            })
        return f"SUCCESS: Saved to AlloyDB. Date: {log_date}, Metric: {metric}"
    except Exception as e:
        return f"ERROR: DB save failed. {e}"

def retrieve_from_database(target_date: str) -> str:
    """Retrieves clinical logbook entries from the AlloyDB database for a specific date (YYYY-MM-DD)."""
    try:
        with engine.begin() as conn:
            query = text("SELECT entry_type, metric_value, details FROM clinical_logs WHERE log_date = :target_date")
            result = conn.execute(query, {"target_date": target_date}).fetchall()
            
            if not result:
                return f"No records found for {target_date}."
            
            records = [f"- {row[0]}: {row[1]} ({row[2]})" for row in result]
            return f"Records for {target_date}:\n" + "\n".join(records)
    except Exception as e:
        return f"ERROR: DB retrieval failed. {e}"

def sync_to_google_calendar(shift_date: str, shift_type: str, location: str) -> str:
    """Syncs a duty roster to the Google Calendar."""
    try:
        service = get_calendar_service()
        
        start_time = datetime.fromisoformat(shift_date)
        end_time = start_time + timedelta(days=1)

        event = {
            'summary': shift_type,
            'location': location,
            'start': { 'date': start_time.strftime('%Y-%m-%d'), 'timeZone': 'Asia/Kolkata' },
            'end': { 'date': end_time.strftime('%Y-%m-%d'), 'timeZone': 'Asia/Kolkata' },
        }

        event = service.events().insert(calendarId='primary', body=event).execute()
        return f"SUCCESS: Event created: {event.get('htmlLink')}"
    except HttpError as error:
        return f"ERROR: Could not create calendar event: {error}"
    except Exception as e:
        return f"ERROR: An unexpected error occurred: {e}"

# --- 1. Clinical Researcher Agent ---
clinical_researcher = Agent(
    name="clinical_researcher",
    model=model_name,
    instruction=f"""
    You are a Medical Data Researcher. Today's date is {datetime.now().strftime('%Y-%m-%d')}.
    Analyze the RAW_INPUT.
    - If it's a NEW WORKLOG: Extract date, entry_type, metric, details.
    - If it's a SCHEDULE: Extract shift_date, shift_type, location.
    - If it's a QUESTION about past data (e.g., "What did I do today?"): Identify the target_date to query.
    Output a JSON summary of your findings and the intent (SAVE, SCHEDULE, or QUERY).
    RAW_INPUT: {{ RAW_INPUT }}
    """,
    output_key="extracted_data"
)

# --- 2. Logbook Formatter Agent ---
logbook_formatter = Agent(
    name="logbook_formatter",
    model=model_name,
    tools=[save_to_database, sync_to_google_calendar, retrieve_from_database],
    instruction="""
    You are the JR Journal Assistant. Take the EXTRACTED_DATA and execute the correct tool.
    - If intent is SAVE: use 'save_to_database'.
    - If intent is SCHEDULE: use 'sync_to_google_calendar'.
    - If intent is QUERY: use 'retrieve_from_database' to look up the data, then summarize it for the doctor.
    Reply in a calm, professional tone.
    EXTRACTED_DATA: { extracted_data }
    """
)

# --- 3. Sequential Workflow ---
jr_journal_workflow = SequentialAgent(
    name="jr_journal_workflow",
    description="Workflow to research and execute clinical tasks.",
    sub_agents=[clinical_researcher, logbook_formatter]
)

# --- 4. Root Agent ---
root_agent = Agent(
    name="jr_journal_greeter",
    model=model_name,
    description="Main entry point.",
    instruction="Save input to state, then transfer to jr_journal_workflow.",
    tools=[add_entry_to_state],
    sub_agents=[jr_journal_workflow]
)
