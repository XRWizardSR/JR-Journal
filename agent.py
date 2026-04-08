import os
import logging
import google.cloud.logging
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.agents import SequentialAgent
from google.adk.tools.tool_context import ToolContext
from google.adk.tools.langchain_tool import LangchainTool

# --- Setup ---
cloud_logging_client = google.cloud.logging.Client()
cloud_logging_client.setup_logging()
load_dotenv()
model_name = os.getenv("MODEL", "gemini-2.5-flash")

# --- Tools ---
def add_entry_to_state(tool_context: ToolContext, doctor_input: str) -> dict[str, str]:
    """Saves the doctor's unstructured input to the workflow state."""
    tool_context.state["RAW_INPUT"] = doctor_input
    logging.info(f"[State updated] Medical input saved: {doctor_input}")
    return {"status": "success"}

# --- 1. Clinical Researcher Agent ---
clinical_researcher = Agent(
    name="clinical_researcher",
    model=model_name,
    instruction="""
    You are a Medical Data Researcher. Analyze the RAW_INPUT from the Junior Resident.
    - Identify if this is a WORKLOG (samples, rounds, metrics) or a SCHEDULE (duty dates, night duty).
    - Extract specific metrics (e.g., 750 samples) and dates.
    - Output a clean summary of findings.

    RAW_INPUT: { RAW_INPUT }
    """,
    output_key="extracted_data"
)

# --- 2. Logbook Formatter Agent ---
logbook_formatter = Agent(
    name="logbook_formatter",
    model=model_name,
    instruction="""
    You are the JR Journal Assistant. Take the EXTRACTED_DATA and finalize the action.
    - If it's a worklog, confirm it has been digitized for the MD Microbiology logbook.
    - If it's a duty date, confirm it's tracked in the roster.
    - Maintain a 'Clinical Ethereal' tone: calm, editorial, and professional.

    EXTRACTED_DATA: { extracted_data }
    """
)

# --- 3. Sequential Workflow ---
jr_journal_workflow = SequentialAgent(
    name="jr_journal_workflow",
    description="Workflow to research and then format clinical entries.",
    sub_agents=[clinical_researcher, logbook_formatter]
)

# --- 4. Root Agent (The Entry Point) ---
agent = Agent(
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