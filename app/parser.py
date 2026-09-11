import re
import pandas as pd
from io import StringIO

# Matches patterns like: "12/05/23, 14:32 - Alice: Hey!" or "[12/05/23, 14:32:05] Alice: Hey!"
DATE_REGEX = r'^(?:\[?(\d{1,2}[\/\.-]\d{1,2}[\/\.-]\d{2,4}),?\s+(\d{1,2}:\d{2}(?::\d{2})?(?:\s?[AP]M)?)\]?)\s+-\s+([^:]+):\s+(.*)$'

def parse_whatsapp_txt(file_bytes: bytes) -> pd.DataFrame:
    text = file_bytes.decode("utf-8", errors="ignore")
    lines = text.splitlines()
    
    parsed_data = []
    
    for line in lines:
        match = re.match(DATE_REGEX, line, re.IGNORECASE)
        if match:
            date_str, time_str, sender, message = match.groups()
            parsed_data.append({
                "raw_datetime": f"{date_str} {time_str}",
                "sender": sender.strip(),
                "message": message.strip()
            })
        elif parsed_data:
            # Handle multi-line messages by appending to previous message
            parsed_data[-1]["message"] += f"\n{line.strip()}"

    df = pd.DataFrame(parsed_data)
    if df.empty:
        raise ValueError("Could not parse file. Ensure it is a valid WhatsApp export.")

    df["timestamp"] = pd.to_datetime(df["raw_datetime"], format="mixed", errors="coerce")
    df = df.dropna(subset=["timestamp"]).sort_values("timestamp").reset_index(drop=True)
    
    return df[["timestamp", "sender", "message"]]

# In app/parser.py
import re

def normalize_sender_name(name: str) -> str:
    """Strips contact tags, nicknames, and special characters."""
    clean_name = re.sub(r'[^a-zA-Z0-9]', '', name).lower()
    if "jisna" in clean_name:
        return "Jisna"
    if "mithra" in clean_name:
        return "Mithra"
    return name.strip()