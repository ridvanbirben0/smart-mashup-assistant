"""
Live DJ Assistant Module
Provides real-time harmonic track recommendation and an interactive CLI interface.
"""

from typing import Optional
import pandas as pd
from .model import get_camelot_neighbors


def recommend_tracks(
    df: pd.DataFrame,
    target_bpm: float,
    target_key: str,
    bpm_tolerance: float = 3.0,
    n_recommendations: int = 5,
    include_neighbors: bool = False,
) -> pd.DataFrame:
    target_key = str(target_key).strip().upper()
    valid_keys = get_camelot_neighbors(target_key) if include_neighbors else {target_key}

    matching = df[
        (df["mik_key_camelot"].isin(valid_keys)) &
        (df["mik_bpm"] >= target_bpm - bpm_tolerance) &
        (df["mik_bpm"] <= target_bpm + bpm_tolerance)
    ].copy()

    if matching.empty:
        return pd.DataFrame()

    matching["bpm_diff"] = (matching["mik_bpm"] - target_bpm).abs()
    matching = matching.sample(frac=1, random_state=42).sort_values(by="bpm_diff")

    candidates = matching.head(min(n_recommendations, len(matching)))
    display_df = candidates[["artist", "title", "mik_bpm", "mik_key_camelot"]].copy()
    display_df = display_df.rename(
        columns={
            "artist": "Artist",
            "title": "Track Title",
            "mik_bpm": "BPM",
            "mik_key_camelot": "Key",
        }
    )
    return display_df


def run_interactive_assistant(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("🎧 SMART MASHUP ASSISTANT - LIVE DJ TERMINAL 🎧")
    print("Harmonic Mixing & BPM Transition Assistant")
    print("=" * 60)

    while True:
        try:
            bpm_input = input("\nEnter current BPM (e.g. 124 or 126.5): ").strip()
            if not bpm_input:
                continue
            target_bpm = float(bpm_input)

            target_key = input("Enter current Camelot Key (e.g. 8A, 5B): ").strip().upper()
            if not target_key:
                print("⚠️ Key cannot be empty.")
                continue

        except ValueError:
            print("⚠️ Invalid input! Please enter a numeric BPM value.")
            continue

        print(f"\n🔍 Searching for compatible tracks at {target_bpm:.1f} BPM in {target_key}...")
        results = recommend_tracks(df, target_bpm, target_key, bpm_tolerance=3.0, n_recommendations=5)

        if results.empty:
            print(f"❌ No exact matches found for {target_key} at {target_bpm} ± 3 BPM.")
            print("💡 Searching with harmonic Camelot neighbors (relative major/minor & adjacent)...")
            results = recommend_tracks(
                df, target_bpm, target_key, bpm_tolerance=3.0, n_recommendations=5, include_neighbors=True
            )

        if results.empty:
            print("❌ Still no tracks found in this tempo window.")
        else:
            print("\n" + "-" * 60)
            print(f"🎵 TOP {len(results)} COMPATIBLE TRACKS (Sorted by Minimal Tempo Pitch Shift):")
            print("-" * 60)
            for idx, row in enumerate(results.itertuples(), 1):
                print(f"{idx}. {row.Artist} - {row._2} | BPM: {row.BPM:.2f} | Key: {row.Key}")
            print("-" * 60)

        choice = input("\nPerform another search? ([Y]/n): ").strip().lower()
        if choice in ("n", "no", "q", "exit"):
            print("\n👋 Exiting Smart Mashup Assistant. Have a great set!\n")
            break
