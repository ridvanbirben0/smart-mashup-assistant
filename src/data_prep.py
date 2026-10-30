"""
Data Preparation & Engineering Module
Handles loading, merging, leakage prevention, and cleaning of DJ audio datasets.
"""

from typing import Tuple
import pandas as pd


def load_raw_data(features_path: str, tracks_path: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    features_df = pd.read_csv(features_path, on_bad_lines="skip")
    tracks_df = pd.read_csv(tracks_path, on_bad_lines="skip")
    return features_df, tracks_df


def clean_and_prepare_dataset(
    features_df: pd.DataFrame, tracks_df: pd.DataFrame
) -> pd.DataFrame:
    df_merged = pd.merge(tracks_df, features_df, on="track_id", how="inner")

    drop_columns = [
        "isrc",
        "year",
        "mik_energy",
        "duration_s",
        "remixer",
        "record_label",
        "mix",
    ]
    existing_drops = [col for col in drop_columns if col in df_merged.columns]
    df_cleaned = df_merged.drop(columns=existing_drops)
    df_cleaned = df_cleaned.dropna()
    return df_cleaned


def get_model_features(
    df_clean: pd.DataFrame,
) -> Tuple[pd.DataFrame, pd.Series]:
    y = df_clean["mik_key_camelot"]

    leakage_and_metadata = [
        "mik_key_camelot",
        "mik_key",
        "harmoniq_key_camelot",
        "harmoniq_key",
        "track_id",
        "artist",
        "title",
        "source",
        "key_agreement",
        "genre",
        "genre_source",
        "harmoniq_confidence",
        "harmoniq_second_key_camelot",
    ]

    columns_to_drop = [col for col in leakage_and_metadata if col in df_clean.columns]
    X = df_clean.drop(columns=columns_to_drop)
    X = X.select_dtypes(include=["number"])
    return X, y
