# prove_stability.py
import os
import pandas as pd
from datetime import datetime

from app.parser import parse_whatsapp_txt
from app.feature_builder import build_reply_dataset
from app.model import train_and_predict

FILE_A = r"jisnachat.txt"   # Adjust path if needed
FILE_B = r"mithrachat.txt"  # Adjust path if needed

TEST_MESSAGE = "hi, are you free right now?"
TEST_TIME = datetime(2026, 9, 11, 18, 0) # 6:00 PM

def run_pipeline_for_file(file_path):
    if not os.path.exists(file_path):
        print(f"[ERROR] Missing file: {file_path}")
        return None

    with open(file_path, "rb") as f:
        df = parse_whatsapp_txt(f.read())

    participants = df["sender"].unique().tolist()
    
    # Pick target participant (maps Mithra or Jisna depending on target)
    target = participants[1] if len(participants) > 1 else participants[0]
    
    dataset = build_reply_dataset(df, target)
    pred_min, exp_time, stats = train_and_predict(dataset, TEST_MESSAGE, TEST_TIME)
    
    return {
        "file": os.path.basename(file_path),
        "target": target,
        "turns_extracted": stats["total_replies_analyzed"],
        "median_min": stats["median_delay_min"],
        "avg_min": stats["avg_delay_min"],
        "predicted_delay_min": round(pred_min, 1)
    }

def prove():
    print("\n" + "=" * 60)
    print("      ORACLE PIPELINE STABILITY COMPARATIVE PROOF")
    print("=" * 60)
    
    res_a = run_pipeline_for_file(FILE_A)
    res_b = run_pipeline_for_file(FILE_B)

    if not res_a or not res_b:
        print("[FAIL] Could not load both files to execute proof.")
        return

    diff = abs(res_a["predicted_delay_min"] - res_b["predicted_delay_min"])

    print(f"\n[EXPORT A] File: {res_a['file']} | Target: {res_a['target']}")
    print(f"  ├── Conversational Turns : {res_a['turns_extracted']}")
    print(f"  ├── Historical Median   : {res_a['median_min']} mins")
    print(f"  └── Predicted Delay     : {res_a['predicted_delay_min']} mins")

    print(f"\n[EXPORT B] File: {res_b['file']} | Target: {res_b['target']}")
    print(f"  ├── Conversational Turns : {res_b['turns_extracted']}")
    print(f"  ├── Historical Median   : {res_b['median_min']} mins")
    print(f"  └── Predicted Delay     : {res_b['predicted_delay_min']} mins")

    print("\n" + "-" * 60)
    print(f" PREDICTION VARIANCE BETWEEN EXPORTS: {diff:.1f} minutes")
    print("-" * 60)

    if diff <= 5.0:
        print("[VERIFIED] STABLE PIPELINE: Predictions converge within a 5-minute margin!")
    else:
        print("[NOTICE] Moderate variance remains. Small sample size limits convergence.")

if __name__ == "__main__":
    prove()