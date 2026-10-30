#!/usr/bin/env python3
"""
Smart Mashup Assistant - Main Entrypoint
CLI application for training the Decision Tree Key Classifier
and running the interactive live DJ transition assistant.
"""

import argparse
import os
import sys
from src.data_prep import load_raw_data, clean_and_prepare_dataset, get_model_features
from src.model import train_key_classifier
from src.assistant import recommend_tracks, run_interactive_assistant


def resolve_data_paths(data_dir: str):
    candidates = [
        (os.path.join(data_dir, "features.csv"), os.path.join(data_dir, "tracks.csv")),
        ("data/features.csv", "data/tracks.csv"),
        ("../data/features.csv", "../data/tracks.csv"),
        (
            "user_uploaded_files/ttl=63d/user_uploaded/features.csv",
            "user_uploaded_files/ttl=63d/user_uploaded/tracks.csv",
        ),
        (
            "../user_uploaded_files/ttl=63d/user_uploaded/features.csv",
            "../user_uploaded_files/ttl=63d/user_uploaded/tracks.csv",
        ),
    ]

    for feat_p, track_p in candidates:
        if os.path.exists(feat_p) and os.path.exists(track_p):
            return feat_p, track_p

    return os.path.join(data_dir, "features.csv"), os.path.join(data_dir, "tracks.csv")


def main():
    parser = argparse.ArgumentParser(
        description="Smart Mashup Assistant: Machine Learning Harmonic DJ Tool"
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Directory containing features.csv and tracks.csv",
    )
    parser.add_argument(
        "--train",
        action="store_true",
        help="Train the Decision Tree model and print accuracy metrics",
    )
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Launch interactive live DJ assistant CLI",
    )
    parser.add_argument(
        "--bpm",
        type=float,
        default=None,
        help="Target BPM for direct CLI query (e.g., 125.0)",
    )
    parser.add_argument(
        "--key",
        type=str,
        default=None,
        help="Target Camelot Key for direct CLI query (e.g., 8A)",
    )

    args = parser.parse_args()

    features_path, tracks_path = resolve_data_paths(args.data_dir)

    if not (os.path.exists(features_path) and os.path.exists(tracks_path)):
        print(f"❌ Error: Dataset files not found in '{args.data_dir}'!")
        print("Please place 'features.csv' and 'tracks.csv' into the 'data/' folder.")
        print("Refer to data/README.md for download instructions from Kaggle or Google Drive.")
        sys.exit(1)

    print(f"📦 Loading datasets from:\n   Features: {features_path}\n   Tracks:   {tracks_path}")
    features_df, tracks_df = load_raw_data(features_path, tracks_path)
    df_clean = clean_and_prepare_dataset(features_df, tracks_df)
    print(f"✅ Master dataset ready: {len(df_clean):,} tracks with clean acoustic features.")

    if args.bpm is not None and args.key is not None:
        print(f"\n🎧 Searching for matches for {args.bpm} BPM and Key {args.key}...")
        results = recommend_tracks(df_clean, args.bpm, args.key, bpm_tolerance=3.0, n_recommendations=5)
        if results.empty:
            print("No exact matches found. Searching with harmonic neighbors...")
            results = recommend_tracks(df_clean, args.bpm, args.key, bpm_tolerance=3.0, n_recommendations=5, include_neighbors=True)
        print("\n" + results.to_string(index=False))
        return

    if args.train:
        print("\n🧠 Extracting features and training Decision Tree Key Classifier...")
        X, y = get_model_features(df_clean)
        try:
            model, metrics, sample_df = train_key_classifier(X, y)
        except ImportError as e:
            print(f"⚠️ {e}")
            return

        print("\n" + "=" * 55)
        print("📊 MODEL PERFORMANCE SUMMARY")
        print("=" * 55)
        print(f"Exact Accuracy:     {metrics['exact_accuracy'] * 100:.2f}%")
        print(f"Harmonic Accuracy:  {metrics['harmonic_accuracy'] * 100:.2f}% (Exact + Compatible Neighbors)")
        print(f"Training Samples:   {metrics['train_samples']:,}")
        print(f"Test Samples:       {metrics['test_samples']:,}")
        print(f"Acoustic Features:  {metrics['feature_count']}")
        print("=" * 55)
        print("\n🔍 Sample Predictions vs Ground Truth:")
        print(sample_df.to_string(index=False))
        print("=" * 55)
        return

    if args.interactive:
        run_interactive_assistant(df_clean)
        return

    print("\n🎧 Sample DJ Recommendation Query (125.0 BPM, Key: 8A):")
    sample_recs = recommend_tracks(df_clean, 125.0, "8A", bpm_tolerance=3.0, n_recommendations=5)
    print(sample_recs.to_string(index=False))
    print("\n💡 Tip: Run 'python main.py --interactive' for live DJ transition mode.")
    print("💡 Tip: Run 'python main.py --train' to train and evaluate the Decision Tree model.")


if __name__ == "__main__":
    main()
