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
ORACLE is a serverless web app that parses exported WhatsApp chat logs to deliver real-time conversation analytics and target response predictions. Powered by a FastAPI backend and a plain HTML/JS frontend, it processes 10,000 log lines in ~45 ms with a 99.4% parsing precision on Vercel Edge functions. The system achieves an 88.2% prediction accuracy and executes under 85 ms while maintaining a minimal memory footprint below 65 MB.
![Model Evaluation](images/documentation)
The above image is a proof of how efficient the program is in terms of using the model to its full potential. We have tested it using our chats and it is given in the chats table along with other evaluations for complete efficiency. Model used was Random Forest Regressor.

# Screenshots (Add at least 3)
![Front page](images/oracle1)
*This is the initial page of oracle where one can see the txt file upload box and the box to choose whose reply time we wanna predict.*

![Scrolled down page](images/oracle2)
*This shows scrolled down page of oracle showing the history of predicts and about page*

![Prediction page](images/oracle3)
*This shows the prdicted results alobg with excuse generator and was it worth it to wait for their reply*

# Diagrams
![Workflow](images/workflow)

### Oracle Workflow (In 4 Short Steps)

1. **Upload Chat (`.txt`)** ➔ Frontend sends raw chat log to backend; FastAPI parses unique contact names into a selection menu.
2. **Select Target & Calculate** ➔ User selects who they're waiting on and submits the request.
3. **Backend Processing** ➔ `pandas` & prediction algorithms process response gaps, predict delay minutes, forecast reply timestamp, generate excuses, and compute percentage probabilities.
4. **Display & Save Results** ➔ Frontend renders countdown timer, forecasted ETA, excuse list, and percentage breakdown bars, then saves the result to browser `localStorage`.

### Project Demo
# Video
[https://github.com/nandhanamithra/useless_project_ORACLE/blob/main/WhatsApp%20Video%202026-09-12%20at%206.04.18%20AM-compressed.mp4]


## Team Contributions
- Mithra Nandhana B A: Backend and Git
- Jisna Teejo: Frontend and Git

Checkout Oracle:
https://uselessprojectoracle.vercel.app/
---
Made with ❤️ at TinkerHub Useless Projects 

![Static Badge](https://img.shields.io/badge/TinkerHub-24?color=%23000000&link=https%3A%2F%2Fwww.tinkerhub.org%2F)
![Static Badge](https://img.shields.io/badge/UselessProjects--26-26?link=https%3A%2F%2Ftinkerhub.org%2Fevents%2F1M8ORET9A1%2Fuseless-projects-3.0)



