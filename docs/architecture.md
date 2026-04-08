graph TD
    %% User Interaction
    User((Doctor / User)) -- "Voice/Text Command" --> API[API Gateway Cloud Run]
    
    %% Primary Agent
    API -- "Forwards Request" --> PrimaryAgent{Chief Resident Agent}
    
    %% Sub-Agents
    PrimaryAgent -- "Schedule/Roster Task" --> ScheduleAgent[Scheduling Sub-Agent]
    PrimaryAgent -- "Worklog/Clinical Task" --> LogbookAgent[Logbook Sub-Agent]
    
    %% Tools & MCP Integration
    ScheduleAgent -- "MCP Integration" --> Calendar[(Google Calendar API)]
    LogbookAgent -- "MCP Integration" --> DB[(AlloyDB / PostgreSQL)]
    
    %% Feedback Loop
    Calendar -. "Confirmation" .-> ScheduleAgent
    DB -. "Saved Record" .-> LogbookAgent
    ScheduleAgent -. "Success" .-> PrimaryAgent
    LogbookAgent -. "Success" .-> PrimaryAgent
    PrimaryAgent -. "Final Response" .-> User

    %% Styling
    classDef agent fill:#f9f,stroke:#333,stroke-width:2px;
    classDef db fill:#bbf,stroke:#333,stroke-width:2px;
    class PrimaryAgent,ScheduleAgent,LogbookAgent agent;
    class Calendar,DB db;