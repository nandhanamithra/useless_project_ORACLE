# test/test_features.py
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
from app.worth_the_wait import calculate_worth_the_wait_and_probabilities

FILE_PATH = os.path.join(PROJECT_ROOT, "txt file\jisnachat.txt")


def test_interactive_features():
    if not os.path.exists(FILE_PATH):
        print(f"[ERROR] Chat file not found at: {FILE_PATH}")
        return

    print("\n" + "=" * 60)
    print("      ORACLE BACKEND FEATURES INTERACTIVE TESTER")
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
        target_person = participants[1] if len(participants) > 1 else participants[0]

    # 3. Interactive Message Input
    custom_msg = input("\nEnter message to test (press Enter for default 'hi'): ").strip()
    if not custom_msg:
        custom_msg = "hi"

    print("\n" + "-" * 60)
    print(f" Running Analysis for Target Person: '{target_person}'")
    print("-" * 60)

    # 4. Model Prediction
    dataset = build_reply_dataset(df, target_person)
    now = datetime.now()
    pred_min, exp_time, stats = train_and_predict(dataset, custom_msg, now)

    # 5. Feature 1: Contextual & Historical Excuses
    excuses = generate_excuses(
        df=df,
        target_person=target_person,
        predicted_delay_min=pred_min,
        send_time=now,
        count=3
    )

    # 6. Feature 2: Worth the Wait & Behavioral Probabilities
    worth_data = calculate_worth_the_wait_and_probabilities(
        predicted_delay_min=pred_min,
        historical_median_min=stats["median_delay_min"],
        incoming_msg=custom_msg,
        send_time=now
    )

    # Output Results
    print(f"\n--- PREDICTION OUTPUT ---")
    print(f"  Target Person   : {target_person}")
    
    print(f"\n--- WORTH THE WAIT? ---")
    print(f"  Verdict : {worth_data['worth_the_wait']['verdict']}")
    print(f"  Advice  : {worth_data['worth_the_wait']['advice']}")

    print(f"\n--- BEHAVIORAL PROBABILITIES ---")
    for item in worth_data["probabilities"]:
        print(f"  • {item['label']:<32} : {item['percentage']}%")


    print("\n" + "=" * 60)


if __name__ == "__main__":
    test_interactive_features()