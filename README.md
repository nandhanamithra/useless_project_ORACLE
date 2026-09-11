<img width="1280" height="640" alt="git (1)" src="https://github.com/user-attachments/assets/8920b256-2ba8-4988-b824-5351134eb4bd" />



# ORACLE- The Reply Time Predictor 🎯


## Basic Details
### Team Name: Aurora


### Team Members
- Team Lead: Mithra Nandhana B A - RIT KOTTAYAM
- Member 2: Jisna Teejo - RIT KOTTAYAM

### Project Description
Oracle is an interactive, data-driven web app designed to dissect message response habits from uploaded chat exports. By feeding your WhatsApp chat files into Oracle's machine learning model, it analyzes message intervals, participant interaction speed, and historical texting trends to calculate exact expected reply times, breakdown probability stats on why you are being left on read, and predict the most likely excuses you are about to receive.

### The Problem (that doesn't exist)
In an era dominated by instant communication, millions of people suffer from severe Delusional Optimism Disorder (DOD)—the ungrounded belief that a text left on "Delivered" for four hours means the recipient is merely drafting a thoughtful, multi-paragraph response. Humanity lacks an objective, cold-hearted arbiter to destroy these delusions with brutal statistical probability. Without automated oversight, overthinkers spend hours analyzing double-checks, formulating wild conspiracy theories, and assuming their contacts have either been abducted by aliens or fallen into an unrecoverable coma.[What ridiculous problem are you solving?]

### The Solution (that nobody asked for)
Enter Oracle: the digital reality-check no one requested, but everyone secretly needs! Simply upload your chat logs, and Oracle's mathematical engine strips away your emotional bias to answer the ultimate question: Are they actually busy, or are they actively ignoring you? By running machine learning algorithms on past response delays, Oracle calculates precise, unvarnished expected reply times, exposes historical ghosting patterns, and generates custom, highly accurate excuses. It turns painful texting anxieties into quantified, interactive data—finally giving you hard evidence that, yes, they are on their phone right now.

## Technical Details
### Technologies/Components Used
For Software:
- Languages
  Python, HTML, CSS. JavaScript
- Frameworks
  Backend: FastAPI 
  Frontend: Bootstrap 5.3.8
- Libraries
  pandas, random, fast api, numpy, sklearn, re, io, datetime
- Tools
  Uvicorn, REST API, CORS MIDDLEWARE, Git, VSCode 

For Hardware: nil

### Implementation
# Clone the repository
git clone https://github.com/your-username/oracle.git
cd oracle

# Create and activate a virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Installation
pip install -r requirements.txt

# Run
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000

### Project Documentation
For Software:

# Screenshots (Add at least 3)
![Screenshot1](Add screenshot 1 here with proper name)
*Add caption explaining what this shows*

![Screenshot2](Add screenshot 2 here with proper name)
*Add caption explaining what this shows*

![Screenshot3](Add screenshot 3 here with proper name)
*Add caption explaining what this shows*

# Diagrams
flowchart TD
    %% Styling
    classDef client fill:#15183d,stroke:#a855f7,stroke-width:2px,color:#fff
    classDef api fill:#111334,stroke:#06b6d4,stroke-width:2px,color:#fff
    classDef process fill:#1a103c,stroke:#ec4899,stroke-width:1px,color:#fff

    subgraph Client ["Frontend (Browser UI)"]
        A[User Uploads WhatsApp .txt Export]:::client
        C[Populate Target Senders Dropdown]:::client
        D[User Selects Target Person & Triggers Calculation]:::client
        H[Render Timer, Timestamp, Excuses & Breakdown Bars]:::client
        I[Save Session to LocalStorage History]:::client
    end

    subgraph Backend ["FastAPI Backend (Python)"]
        B["/api/v1/parse-participants"]:::api
        E["/predict"]:::api
        
        subgraph Pipeline ["Processing Pipeline"]
            F1["parse_whatsapp_txt()<br>Extract DataFrame"]:::process
            F2["build_reply_dataset()<br>Feature Engineering"]:::process
            F3["train_and_predict()<br>Calculate Response Delay"]:::process
            F4["generate_excuses()<br>Generate History Grounded Excuses"]:::process
            F5["Calculate Probability Breakdown (%)"]:::process
        end
    end

    %% User Flow Connections
    A -->|1. POST File| B
    B --> F1
    F1 -->|Return Sender List| C
    C --> D
    D -->|2. POST File + Target| E
    
    %% Processing Pipeline Connections
    E --> F1
    F1 --> F2
    F2 --> F3
    F3 --> F4
    F4 --> F5
    
    %% Result Return
    F5 -->|3. Return JSON Payload| H
    H --> I

### Oracle Workflow (In 4 Short Steps)

1. **Upload Chat (`.txt`)** ➔ Frontend sends raw chat log to backend; FastAPI parses unique contact names into a selection menu.
2. **Select Target & Calculate** ➔ User selects who they're waiting on and submits the request.
3. **Backend Processing** ➔ `pandas` & prediction algorithms process response gaps, predict delay minutes, forecast reply timestamp, generate excuses, and compute percentage probabilities.
4. **Display & Save Results** ➔ Frontend renders countdown timer, forecasted ETA, excuse list, and percentage breakdown bars, then saves the result to browser `localStorage`.


# Schematic & Circuit
![Circuit](Add your circuit diagram here)
*Add caption explaining connections*

![Schematic](Add your schematic diagram here)
*Add caption explaining the schematic*

# Build Photos
![Components](Add photo of your components here)
*List out all components shown*

![Build](Add photos of build process here)
*Explain the build steps*

![Final](Add photo of final product here)
*Explain the final build*

### Project Demo
# Video
[Add your demo video link here]
*Explain what the video demonstrates*

# Additional Demos
[Add any extra demo materials/links]

## Team Contributions
- [Name 1]: [Specific contributions]
- [Name 2]: [Specific contributions]
- [Name 3]: [Specific contributions]

---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



