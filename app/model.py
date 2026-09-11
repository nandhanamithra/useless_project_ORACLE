# app/model.py
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

def train_and_predict(dataset: pd.DataFrame, incoming_msg: str, send_time: datetime):
    feature_cols = [
        "hour", 
        "day_of_week", 
        "is_weekend", 
        "incoming_msg_len", 
        "is_late_night", 
        "is_work_hours"
    ]
    
    X = dataset[feature_cols]
    y_raw = dataset["target_delay_minutes"]
    y_log = np.log1p(y_raw)
    
    n_samples = len(dataset)
    median_delay = float(y_raw.median())

    # Train model
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=3,
        min_samples_leaf=2,
        random_state=42
    )
    model.fit(X, y_log)
    
    # Inference vector
    day_of_week_val = send_time.weekday()
    hour_val = send_time.hour
    
    input_features = pd.DataFrame([{
        "hour": hour_val,
        "day_of_week": day_of_week_val,
        "is_weekend": 1 if day_of_week_val >= 5 else 0,
        "incoming_msg_len": len(incoming_msg),
        "is_late_night": 1 if (hour_val >= 23 or hour_val < 6) else 0,
        "is_work_hours": 1 if (9 <= hour_val <= 17 and day_of_week_val < 5) else 0
    }])
    
    # Model prediction
    pred_log = model.predict(input_features)[0]
    model_pred_min = max(0.0, float(np.expm1(pred_log)))

    # BLENDING: For small sample sizes, anchor the model prediction with the true median
    if n_samples < 25:
        # 50% model prediction + 50% median delay
        final_delay_min = (0.5 * model_pred_min) + (0.5 * median_delay)
    else:
        final_delay_min = model_pred_min

    expected_reply_time = send_time + timedelta(minutes=final_delay_min)
    
    stats = {
        "total_replies_analyzed": int(n_samples),
        "median_delay_min": round(median_delay, 1),
        "avg_delay_min": round(float(y_raw.mean()), 1),
        "fastest_reply_min": round(float(y_raw.min()), 1),
        "slowest_reply_min": round(float(y_raw.max()), 1)
    }
    
    return final_delay_min, expected_reply_time, stats