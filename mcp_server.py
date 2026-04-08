import os
from mcp.server.fastmcp import FastMCP
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

# --- Database Connection (AlloyDB) ---
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "postgres")
engine = create_engine(f"postgresql+pg8000://{DB_USER}:{DB_PASS}@{DB_HOST}:5432/{DB_NAME}")

mcp = FastMCP("JRJournalClinicalTools")

@mcp.tool()
def save_clinical_log(log_date: str, entry_type: str, metric: int, details: str) -> str:
    """Saves a medical resident's clinical logbook entry into secure AlloyDB."""
    try:
        with engine.begin() as conn:
            query = text("""
                INSERT INTO clinical_logs (log_date, entry_type, metric_value, details) 
                VALUES (:log_date, :entry_type, :metric, :details)
            """)
            conn.execute(query, {"log_date": log_date, "entry_type": entry_type, "metric": metric, "details": details})
        return f"MCP SUCCESS: Digitized log for {log_date}."
    except Exception as e:
        return f"MCP ERROR: {e}"

@mcp.tool()
def retrieve_clinical_logs(target_date: str) -> str:
    """Retrieves medical records from AlloyDB for a specific date (YYYY-MM-DD)."""
    try:
        with engine.begin() as conn:
            query = text("SELECT entry_type, metric_value FROM clinical_logs WHERE log_date = :target_date")
            result = conn.execute(query, {"target_date": target_date}).fetchall()
            if not result: return f"No logs found for {target_date}."
            return f"Found {len(result)} records for {target_date}."
    except Exception as e:
        return f"MCP ERROR: {e}"

if __name__ == "__main__":
    mcp.run()
