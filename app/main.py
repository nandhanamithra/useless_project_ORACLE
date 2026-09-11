from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from datetime import datetime
from app.parser import parse_whatsapp_txt
from app.feature_builder import build_reply_dataset
from app.model import train_and_predict
import random
from app.excuse_generator import generate_excuses
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(title="ORACLE API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/api/v1/parse-participants")
async def get_participants(file: UploadFile = File(...)):
    """Uploads chat file and returns list of unique senders."""
    content = await file.read()
    try:
        df = parse_whatsapp_txt(content)
        participants = df["sender"].unique().tolist()
        return {"participants": participants}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/api/v1/predict")
async def predict_response_time(
    file: UploadFile = File(...),
    target_person: str = Form(...),
    new_message: str = Form(...),
    send_time_iso: str = Form(None)
):
    """Parses chat, trains model on target person, and predicts response delay."""
    content = await file.read()
    
    try:
        # Parse Chat
        df = parse_whatsapp_txt(content)
        
        # Feature Engineering
        dataset = build_reply_dataset(df, target_person)
        
        # Parse timestamp or default to now
        send_dt = datetime.fromisoformat(send_time_iso) if send_time_iso else datetime.now()
        
        # Train & Predict
        delay_min, expected_time, stats = train_and_predict(dataset, new_message, send_dt)
        
        return {
            "target_person": target_person,
            "predicted_delay": {
                "minutes": round(delay_min, 1),
                "formatted": f"{int(delay_min // 60)}h {int(delay_min % 60)}m" if delay_min >= 60 else f"{int(delay_min)} mins"
            },
            "expected_reply_time": expected_time.strftime("%I:%M %p, %a %b %d"),
            "historical_stats": stats
        }
        
    except ValueError as ve:
        raise HTTPException(status_code=422, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
@app.post("/predict")
async def predict_delay(file: UploadFile, target_person: str, message: str = "hi"):
    contents = await file.read()
    df = parse_whatsapp_txt(contents)
    
    dataset = build_reply_dataset(df, target_person)
    
    predicted_delay_min, expected_reply_time, stats = train_and_predict(
        dataset, message, datetime.now()
    )
    
    # Generate history-grounded excuses
    excuses = generate_excuses(
        df=df,
        target_person=target_person,
        predicted_delay_min=predicted_delay_min,
        send_time=datetime.now(),
        count=3
    )

# Generate breakdown percentages
    raw_weights = [random.randint(10, 80) for _ in range(6)]
    total_weight = sum(raw_weights)
    percentages = [round((w / total_weight) * 100) for w in raw_weights]
    percentages[-1] = 100 - sum(percentages[:-1])  # Ensure exact 100% total

    worth_the_wait_breakdown = [
        {"label": "Sleeping", "percentage": percentages[0]},
        {"label": "On their phone but ignoring you", "percentage": percentages[1]},
        {"label": "Busy", "percentage": percentages[2]},
        {"label": "Typing a thoughtful response", "percentage": percentages[3]},
        {"label": "Talking to someone else", "percentage": percentages[4]},
        {"label": "Abducted by aliens", "percentage": percentages[5]}
    ]

    return {
        "target_person": target_person,
        "predicted_delay_min": round(predicted_delay_min, 1),
        "expected_reply_time": expected_reply_time.strftime("%I:%M %p, %a %b %d"),
        "excuses": excuses,
        "worth_the_wait_breakdown": worth_the_wait_breakdown,
        "historical_stats": stats
    }
@app.get("/")
async def root():
    return {"status": "ORACLE API is running"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)