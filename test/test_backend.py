# test_backend.py
import os
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# Path to your actual WhatsApp export file
CHAT_FILE_PATH = r"C:\flutter_projects\ORACLE\useless_project_ORACLE\mithrachat.txt"  # <-- UPDATE THIS PATH

def test_real_chat_file():
    if not os.path.exists(CHAT_FILE_PATH):
        print(f"[ERROR] File not found at: {CHAT_FILE_PATH}")
        print("Please update CHAT_FILE_PATH with a valid path to your WhatsApp export .txt file.")
        return

    print(f"--- 1. Reading file: {os.path.basename(CHAT_FILE_PATH)} ---")
    with open(CHAT_FILE_PATH, "rb") as f:
        file_bytes = f.read()

    files = {"file": ("_chat.txt", file_bytes, "text/plain")}

    # Step A: Parse participants
    print("\n--- 2. Fetching Participants ---")
    response = client.post("/api/v1/parse-participants", files=files)
    assert response.status_code == 200, f"Parse failed: {response.json()}"
    
    participants = response.json()["participants"]
    if not participants:
        print("[ERROR] No participants found in chat log.")
        return

    print(f"[SUCCESS] Found {len(participants)} participants:")
    for i, p in enumerate(participants, 1):
        print(f"  [{i}] {p}")

    # Step B: Let user select or enter the target person
    print("\n--- 3. Select Target Person ---")
    user_choice = input(f"Enter participant number (1-{len(participants)}) or type exact name: ").strip()

    # Determine target_person based on input
    if user_choice.isdigit():
        index = int(user_choice) - 1
        if 0 <= index < len(participants):
            target_person = participants[index]
        else:
            print("[ERROR] Invalid selection number.")
            return
    else:
        target_person = user_choice

    # Step C: Prompt for optional custom text message
    custom_msg = input("\nEnter message to test (press Enter for default): ").strip()
    if not custom_msg:
        custom_msg = "Hey, are you free to chat right now?"

    print(f"\n--- 4. Running Prediction for: '{target_person}' ---")

    payload = {
        "target_person": target_person,
        "new_message": custom_msg,
        "send_time_iso": "2026-09-11T18:00:00"
    }

    # Re-send file bytes in payload for prediction
    files = {"file": ("_chat.txt", file_bytes, "text/plain")}
    response = client.post("/api/v1/predict", files=files, data=payload)

    if response.status_code == 200:
        res = response.json()
        print("\n[SUCCESS] Prediction Output:")
        print(f" Target Person: {res['target_person']}")
        print(f" Predicted Delay: {res['predicted_delay']['formatted']} ({res['predicted_delay']['minutes']} mins)")
        print(f" Expected Reply Time: {res['expected_reply_time']}")
        print(f" Historical Stats: {res['historical_stats']}")
    else:
        print(f"\n[FAILED] Predict endpoint returned status {response.status_code}:")
        print(response.json())

if __name__ == "__main__":
    test_real_chat_file()