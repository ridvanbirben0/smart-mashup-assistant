"""
Smart Mashup Assistant - Core Package
Harmonic Key Prediction and Live DJ Transition Assistant using Machine Learning.
"""

from .data_prep import load_raw_data, clean_and_prepare_dataset, get_model_features
from .model import train_key_classifier, get_camelot_neighbors
from .assistant import recommend_tracks, run_interactive_assistant

__all__ = [
    "load_raw_data",
    "clean_and_prepare_dataset",
    "get_model_features",
    "train_key_classifier",
    "get_camelot_neighbors",
    "recommend_tracks",
    "run_interactive_assistant",
]
