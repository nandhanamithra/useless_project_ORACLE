# app/excuse_generator.py
import re
import random
import pandas as pd
from datetime import datetime

# Common excuse patterns to search for in actual past messages
HISTORICAL_EXCUSE_PATTERNS = {
    "sleep": [r"\bsleep(ing|t)?\b", r"\bbed\b", r"\bnap\b", r"\bnight\b", r"\bpassed out\b"],
    "work_study": [r"\bclass\b", r"\bwork\b", r"\bbusy\b", r"\bmeeting\b", r"\bstudy\b", r"\bexam\b", r"\blab\b"],
    "device_tech": [r"\bdead\b", r"\bcharg(e|ing)\b", r"\bbattery\b", r"\bwifi\b", r"\bphone\b", r"\bsilent\b"],
    "transit_out": [r"\bdriv(e|ing)\b", r"\btravel\b", r"\boutside\b", r"\broad\b", r"\bway\b", r"\btraffic\b"],
    "eating_chores": [r"\bfood\b", r"\beat(ing)?\b", r"\bdinner\b", r"\blunch\b", r"\bcook(ing)?\b"]
}

DEFAULT_BEHAVIORAL_EXCUSES = {
    "late_night": [
        "Usually dormant or sleeping during late-night hours.",
        "Historically mute to notifications past midnight.",
        "High probability of falling asleep mid-chat."
    ],
    "work_hours": [
        "Typically occupied with class, lab, or work commitments.",
        "Habitually leaves phone on silent during active hours.",
        "In a deep focus window based on weekday activity patterns."
    ],
    "general_delay": [
        "Historically takes longer to respond to lengthy messages.",
        "Tends to step away from the phone during peak activity gaps.",
        "Exhibits batch-reply behavior rather than immediate messaging."
    ]
}

def extract_historical_excuses(df: pd.DataFrame, target_person: str) -> list:
    """
    Mines the target person's actual message history for past excuses they have used.
    """
    # Filter strictly for messages sent by the target
    target_msgs = df[df["sender"] == target_person]["message"].dropna().astype(str).tolist()
    
    found_excuses = []
    
    for msg in target_msgs:
        msg_lower = msg.lower()
        
        # Look for short messages containing excuse patterns (e.g., "sorry was sleeping", "in class")
        if len(msg) < 80:
            for category, patterns in HISTORICAL_EXCUSE_PATTERNS.items():
                for pattern in patterns:
                    if re.search(pattern, msg_lower):
                        # Clean up prefix noise like "sorry " or "ah "
                        clean_msg = re.sub(r"^(sorry|sry|ah|oh|hey|haha)[,\s]*", "", msg, flags=re.IGNORECASE).strip()
                        if clean_msg and clean_msg not in found_excuses:
                            found_excuses.append(f'Past habit: Often says "{clean_msg}"')
                        break
                        
    return found_excuses


def generate_excuses(
    df: pd.DataFrame, 
    target_person: str, 
    predicted_delay_min: float, 
    send_time: datetime, 
    count: int = 3
) -> list:
    """
    Generates tailored excuses by combining mined chat phrases with behavioral patterns.
    """
    # 1. Mine actual historical excuses from chat log
    mined_excuses = extract_historical_excuses(df, target_person)
    
    # 2. Extract behavioral patterns based on time and delay duration
    hour = send_time.hour
    day_of_week = send_time.weekday()
    
    is_late_night = (hour >= 23 or hour < 6)
    is_work_hours = (9 <= hour <= 17 and day_of_week < 5)

    behavioral_candidates = []
    
    if is_late_night:
        behavioral_candidates.extend(DEFAULT_BEHAVIORAL_EXCUSES["late_night"])
    elif is_work_hours:
        behavioral_candidates.extend(DEFAULT_BEHAVIORAL_EXCUSES["work_hours"])
    else:
        behavioral_candidates.extend(DEFAULT_BEHAVIORAL_EXCUSES["general_delay"])

    # 3. Blend mined historical phrases with behavioral inferences
    combined_pool = []
    
    # Priority to real phrases mined from their chat history
    if mined_excuses:
        random.shuffle(mined_excuses)
        combined_pool.extend(mined_excuses[:2])  # Take up to 2 real mined phrases
        
    random.shuffle(behavioral_candidates)
    combined_pool.extend(behavioral_candidates)
    
    # Deduplicate while preserving order
    final_excuses = []
    for excuse in combined_pool:
        if excuse not in final_excuses:
            final_excuses.append(excuse)
        if len(final_excuses) == count:
            break
            
    return final_excuses