# app/worth_the_wait.py
from datetime import datetime
import pandas as pd

def calculate_worth_the_wait_and_probabilities(
    predicted_delay_min: float,
    historical_median_min: float,
    incoming_msg: str,
    send_time: datetime
) -> dict:
    """
    Calculates a 'Worth the Wait?' verdict and behavioral probability percentages
    without emojis.
    """
    hour = send_time.hour
    day_of_week = send_time.weekday()
    msg_len = len(incoming_msg)

    is_late_night = (hour >= 23 or hour < 6)
    is_work_hours = (9 <= hour <= 17 and day_of_week < 5)

    # 1. Determine "Worth the Wait?" Verdict & Advice
    if predicted_delay_min <= 5.0:
        verdict = "DEFINITELY YES"
        advice = "They usually reply almost instantly right now. Keep your app open!"
    elif predicted_delay_min <= 20.0:
        verdict = "YES, PROBABLY"
        advice = "Worth hanging around for a few minutes. Grab a glass of water."
    elif predicted_delay_min <= 60.0:
        verdict = "MAYBE NOT"
        advice = "Put your phone down and go do something else. Check back in an hour."
    else:
        verdict = "ABSOLUTELY NOT"
        advice = "Do not wait up! Go to sleep or focus on your own day."

    # 2. Dynamic Behavioral Probability Calculations
    p_aliens = 9.0

    if is_late_night:
        p_sleeping = 55.0
        p_ignoring = 15.0
        p_busy = 10.0
        p_thoughtful = 2.0
        p_talking_others = 9.0
    elif is_work_hours:
        p_sleeping = 3.0
        p_ignoring = 20.0
        p_busy = 48.0
        p_thoughtful = 5.0
        p_talking_others = 15.0
    else:
        p_sleeping = 10.0
        p_ignoring = 35.0
        p_busy = 22.0
        p_thoughtful = 6.0
        p_talking_others = 18.0

    if msg_len > 80:
        p_thoughtful += 10.0
        p_ignoring = max(5.0, p_ignoring - 5.0)

    if predicted_delay_min > (historical_median_min * 1.8):
        p_ignoring += 10.0
        p_busy += 5.0

    raw_total = p_sleeping + p_ignoring + p_busy + p_thoughtful + p_talking_others
    target_total = 100.0 - p_aliens

    p_sleeping = round((p_sleeping / raw_total) * target_total)
    p_ignoring = round((p_ignoring / raw_total) * target_total)
    p_busy = round((p_busy / raw_total) * target_total)
    p_thoughtful = round((p_thoughtful / raw_total) * target_total)
    
    p_talking_others = int(100 - (p_sleeping + p_ignoring + p_busy + p_thoughtful + p_aliens))

    return {
        "worth_the_wait": {
            "verdict": verdict,
            "badge": verdict,
            "advice": advice
        },
        "probabilities": [
            {"label": "Sleeping", "percentage": int(p_sleeping)},
            {"label": "On their phone but ignoring you", "percentage": int(p_ignoring)},
            {"label": "Busy", "percentage": int(p_busy)},
            {"label": "Typing a thoughtful response", "percentage": int(p_thoughtful)},
            {"label": "Talking to someone else", "percentage": int(p_talking_others)},
            {"label": "Abducted by aliens", "percentage": int(p_aliens)}
        ]
    }