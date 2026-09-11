# app/feature_builder.py
import pandas as pd

def build_reply_dataset(df: pd.DataFrame, target_person: str):
    """
    Extracts consecutive non-target -> target reply pairs with time & message features.
    """
    df["message_len"] = df["message"].astype(str).apply(len)
    records = []
    
    i = 0
    n = len(df)
    
    while i < n - 1:
        curr_msg = df.iloc[i]
        
        if curr_msg["sender"] != target_person:
            last_incoming_idx = i
            while last_incoming_idx + 1 < n and df.iloc[last_incoming_idx + 1]["sender"] != target_person:
                last_incoming_idx += 1
                
            next_idx = last_incoming_idx + 1
            if next_idx < n and df.iloc[next_idx]["sender"] == target_person:
                incoming_msg = df.iloc[last_incoming_idx]
                reply_msg = df.iloc[next_idx]
                
                delay_minutes = (reply_msg["timestamp"] - incoming_msg["timestamp"]).total_seconds() / 60.0
                
                # Filter out instant doubles or overnight delays (> 12 hrs)
                if 0.16 <= delay_minutes <= 720:
                    ts = incoming_msg["timestamp"]
                    
                    records.append({
                        "hour": ts.hour,
                        "day_of_week": ts.weekday(),
                        "is_weekend": 1 if ts.weekday() >= 5 else 0,
                        "incoming_msg_len": incoming_msg["message_len"],
                        "is_late_night": 1 if (ts.hour >= 23 or ts.hour < 6) else 0,
                        "is_work_hours": 1 if (9 <= ts.hour <= 17 and ts.weekday() < 5) else 0,
                        "target_delay_minutes": delay_minutes
                    })
            
            i = next_idx
        else:
            i += 1

    dataset = pd.DataFrame(records)
    
    # Filter extreme outliers using IQR
    if len(dataset) >= 15:
        q1 = dataset["target_delay_minutes"].quantile(0.25)
        q3 = dataset["target_delay_minutes"].quantile(0.75)
        iqr = q3 - q1
        upper_bound = q3 + (1.5 * iqr)
        dataset = dataset[dataset["target_delay_minutes"] <= upper_bound]

    if len(dataset) < 5:
        raise ValueError(f"Not enough clean reply pairs found for '{target_person}'.")
    
    # In app/feature_builder.py
    upper_cap = dataset["target_delay_minutes"].quantile(0.90)
    dataset["target_delay_minutes"] = dataset["target_delay_minutes"].clip(upper=upper_cap)
    return dataset

# In app/feature_builder.py
def categorize_msg_len(length: int) -> int:
    if length <= 10:
        return 0  # Short (e.g. "hi", "ok")
    elif length <= 50:
        return 1  # Medium
    return 2      # Long
