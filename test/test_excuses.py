# test/test_excuses.py
import os
import sys
from datetime import datetime

# Dynamically add the project root directory to Python path
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from app.parser import parse_whatsapp_txt
from app.feature_builder import build_reply_dataset
from app.model import train_and_predict
from app.excuse_generator import generate_excuses, extract_historical_excuses

FILE_PATH = os.path.join(PROJECT_ROOT, "txt file\jisnachat.txt")


def test_excuse_pipeline_interactive():
    if not os.path.exists(FILE_PATH):
        print(f"[ERROR] Chat file not found at: {FILE_PATH}")
        return

    print("\n" + "=" * 60)
    print("      ORACLE INTERACTIVE EXCUSE TESTER")
    print(f"      File: {os.path.basename(FILE_PATH)}")
    print("=" * 60)

    # 1. Load and parse chat text
    with open(FILE_PATH, "rb") as f:
        df = parse_whatsapp_txt(f.read())

    participants = df["sender"].unique().tolist()

    # 2. Interactive Participant Selection
    print("\n--- Available Participants ---")
    for idx, name in enumerate(participants, 1):
        print(f" [{idx}] {name}")

    user_choice = input(f"\nSelect target person (1-{len(participants)}) [default 2]: ").strip()

    if user_choice.isdigit() and 1 <= int(user_choice) <= len(participants):
        target_person = participants[int(user_choice) - 1]
    else:
        # Default fallback
        target_person = participants[1] if len(participants) > 1 else participants[0]

    # 3. Interactive Message Input
    custom_msg = input("\nEnter message to test (press Enter for default 'hi'): ").strip()
    if not custom_msg:
        custom_msg = "hi"

    print("\n" + "-" * 60)
    print(f" Running Analysis for Target Person: '{target_person}'")
    print("-" * 60)

    # 4. Mine historical excuse phrases from chat logs
    print("\n--- 1. MINED PAST MESSAGES (From Chat Log) ---")
    mined_phrases = extract_historical_excuses(df, target_person)
    if mined_phrases:
        for phrase in mined_phrases:
            print(f"  • {phrase}")
    else:
        print("  (No direct excuse keywords found in short past messages for this person)")

    # 5. Model prediction & excuse generation
    dataset = build_reply_dataset(df, target_person)
    now = datetime.now()
    pred_min, exp_time, stats = train_and_predict(dataset, custom_msg, now)

    excuses = generate_excuses(
        df=df,
        target_person=target_person,
        predicted_delay_min=pred_min,
        send_time=now,
        count=3
    )

    print(f"\n--- 2. PREDICTED DELAY & GENERATED EXCUSES ---")
    print(f"  Predicted Delay : {pred_min:.1f} minutes")
    print(f"  Expected Reply  : {exp_time.strftime('%I:%M %p, %a %b %d')}\n")
    
    for i, exc in enumerate(excuses, 1):
        print(f"  [{i}] {exc}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_excuse_pipeline_interactive()