# evaluate_model.py
import os
import pandas as pd
import numpy as np

# Import backend business logic directly from app modules
from app.parser import parse_whatsapp_txt
from app.feature_builder import build_reply_dataset

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# 1. Update this path to your WhatsApp chat export file
CHAT_FILE_PATH = r"C:\flutter_projects\ORACLE\useless_project_ORACLE\jisnachat.txt"  # <-- UPDATE FILE PATH HERE

def evaluate_and_plot():
    if not os.path.exists(CHAT_FILE_PATH):
        print(f"[ERROR] File not found: {CHAT_FILE_PATH}")
        return

    print("--- Loading and Parsing Chat File ---")
    with open(CHAT_FILE_PATH, "rb") as f:
        file_bytes = f.read()

    # Parse chat using existing backend module
    df = parse_whatsapp_txt(file_bytes)
    participants = df["sender"].unique().tolist()

    print(f"Found participants: {participants}")
    print("\nSelect target person to evaluate:")
    for i, p in enumerate(participants, 1):
        print(f"  [{i}] {p}")

    choice = input(f"Enter choice (1-{len(participants)}): ").strip()
    target_person = participants[int(choice) - 1] if choice.isdigit() else choice

    print(f"\n--- Extracting Reply Pairs for: {target_person} ---")
    dataset = build_reply_dataset(df, target_person)

    feature_cols = ["hour", "day_of_week", "is_weekend", "incoming_msg_len"]
    X = dataset[feature_cols]
    y = dataset["target_delay_minutes"]

    print(f"Total reply pairs found: {len(X)}")

    if len(X) < 10:
        print("[WARNING] Fewer than 10 samples found. Visualizations may be sparse.")

    # Train / Test Split
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Train Random Forest Regressor
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Make Predictions
    y_pred = model.predict(X_test)

    # Metrics Calculation
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    r2 = r2_score(y_test, y_pred)

    print("\n" + "=" * 45)
    print("         MODEL ACCURACY EVALUATION")
    print("=" * 45)
    print(f" Mean Absolute Error (MAE) : {mae:.2f} minutes off")
    print(f" Root Mean Sq. Error (RMSE): {rmse:.2f} minutes")
    print(f" R² Score                  : {r2:.3f}")
    print("=" * 45)

    # Matplotlib Plotting Section
    try:
        import matplotlib.pyplot as plt

        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

        # -------------------------------------------------------------
        # Subplot 1: Actual vs Predicted Scatter Plot
        # -------------------------------------------------------------
        ax1.scatter(y_test, y_pred, color='#673AB7', alpha=0.7, edgecolors='k', s=60, label='Actual vs Predicted')
        
        # Parity Line (y = x)
        max_val = max(max(y_test) if len(y_test) > 0 else 1, max(y_pred) if len(y_pred) > 0 else 1)
        ax1.plot([0, max_val], [0, max_val], color='#FF5722', linestyle='--', linewidth=2, label='Ideal Line (y=x)')

        ax1.set_title(f'Prediction Accuracy ({target_person})', fontsize=13, fontweight='bold')
        ax1.set_xlabel('Actual Delay (Minutes)', fontsize=11)
        ax1.set_ylabel('Predicted Delay (Minutes)', fontsize=11)
        ax1.legend(loc='upper left')
        ax1.grid(True, linestyle=':', alpha=0.6)

        # -------------------------------------------------------------
        # Subplot 2: Feature Importance Bar Chart
        # -------------------------------------------------------------
        importances = model.feature_importances_
        indices = np.argsort(importances)[::-1]
        sorted_features = [feature_cols[i] for i in indices]
        sorted_importances = importances[indices]

        ax2.bar(sorted_features, sorted_importances, color='#2196F3', edgecolor='k', alpha=0.8)
        ax2.set_title('Feature Importance Breakdown', fontsize=13, fontweight='bold')
        ax2.set_ylabel('Relative Importance', fontsize=11)
        ax2.grid(axis='y', linestyle=':', alpha=0.6)

        # Overall Layout Adjustment
        plt.suptitle(f'ORACLE Model Evaluation Dashboard\nMAE: {mae:.2f} mins | R²: {r2:.3f}', fontsize=15, y=1.02)
        plt.tight_layout()

        # Save High-Res Image for Documentation
        clean_name = target_person.replace(" ", "_").lower()
        output_filename = f"model_evaluation_{clean_name}.png"
        plt.savefig(output_filename, dpi=300, bbox_inches='tight')
        print(f"\n[SUCCESS] Documentation plot saved as: '{output_filename}'")

        plt.show()

    except ImportError:
        print("\n[NOTE] Matplotlib is not installed in this environment.")
        print("Install it by running: pip install matplotlib")

if __name__ == "__main__":
    evaluate_and_plot()