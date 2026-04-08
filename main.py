import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables (.env file)
load_dotenv()

# Initialize the Gemini Client
# Initialize the Gemini Client explicitly using only the GEMINI_API_KEY
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def chief_resident_agent(user_input):
    """
    This is the Primary Agent. It analyzes the doctor's input
    and acts as a router to the specialized sub-agents.
    """
    print("\n[Chief Resident Agent] Analyzing request...")
    
    # We use a system instruction to force the AI to act strictly as a router
    system_instruction = """
    You are the Chief Resident Agent for 'JR Journal', an AI assistant for medical residents. 
    Analyze the user's input and classify it into exactly ONE of these categories:
    1. SCHEDULE: If the user is talking about shifts, night duty, academic rosters, or calendar events.
    2. LOGBOOK: If the user is reporting completed tasks, sample counts (e.g., tested 750 samples), or clinical rounds.
    3. UNKNOWN: If it doesn't fit the above.
    
    Return ONLY the exact category word (SCHEDULE, LOGBOOK, or UNKNOWN). Do not add any other text.
    """
    
    # We use Gemini 2.5 Flash because it is incredibly fast for routing tasks
    response = client.models.generate_content(
        model='gemini-2.5-flash',
        contents=user_input,
        config=types.GenerateContentConfig(
            system_instruction=system_instruction,
            temperature=0.0 # 0.0 means we want strict, factual classification, not creativity
        )
    )
    
    classification = response.text.strip()
    return classification

# A simple terminal loop to test our agent locally
if __name__ == "__main__":
    print("=== JR Journal System Initialized ===")
    print("Type 'exit' to quit.")
    
    while True:
        prompt = input("\nDoctor (You): ")
        if prompt.lower() == 'exit':
            break
            
        task_type = chief_resident_agent(prompt)
        
        if task_type == "SCHEDULE":
            print("[System] -> Routing to Scheduling Sub-Agent... (Integration coming next)")
        elif task_type == "LOGBOOK":
            print("[System] -> Routing to Logbook Sub-Agent... (Integration coming next)")
        else:
            print("[System] -> I didn't understand that. Please specify a schedule or logbook entry.")