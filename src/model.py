"""
Model Training & Harmonic Evaluation Module
Trains a Decision Tree Classifier on acoustic chroma features
and evaluates predictions against musical Camelot Wheel harmony.
"""

from typing import Dict, List, Set, Tuple
import pandas as pd


def get_camelot_neighbors(camelot_key: str) -> Set[str]:
    camelot_key = str(camelot_key).strip().upper()
    if len(camelot_key) < 2:
        return {camelot_key}

    letter = camelot_key[-1]
    try:
        number = int(camelot_key[:-1])
    except ValueError:
        return {camelot_key}

    if letter not in ("A", "B") or not (1 <= number <= 12):
        return {camelot_key}

    opposite_letter = "B" if letter == "A" else "A"
    prev_num = 12 if number == 1 else number - 1
    next_num = 1 if number == 12 else number + 1

    return {
        f"{number}{letter}",            # Same key
        f"{number}{opposite_letter}",   # Relative major/minor
        f"{prev_num}{letter}",          # Adjacent down
        f"{next_num}{letter}",          # Adjacent up
    }


def evaluate_harmonic_accuracy(y_true: pd.Series, y_pred: List[str]) -> float:
    compatible_count = 0
    for true_key, pred_key in zip(y_true, y_pred):
        neighbors = get_camelot_neighbors(true_key)
        if str(pred_key).strip().upper() in neighbors:
            compatible_count += 1
    return compatible_count / len(y_true) if len(y_true) > 0 else 0.0


def train_key_classifier(
    X: pd.DataFrame,
    y: pd.Series,
    test_size: float = 0.2,
    random_state: int = 42,
):
    try:
        from sklearn.model_selection import train_test_split
        from sklearn.tree import DecisionTreeClassifier
        from sklearn.metrics import accuracy_score
    except ImportError:
        raise ImportError(
            "scikit-learn is required for model training. "
            "Please install it using: pip install scikit-learn"
        )

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=random_state
    )

    model = DecisionTreeClassifier(random_state=random_state)
    model.fit(X_train, y_train)

    y_pred = model.predict(X_test)
    exact_acc = accuracy_score(y_test, y_pred)
    harmonic_acc = evaluate_harmonic_accuracy(y_test, y_pred)

    metrics = {
        "exact_accuracy": exact_acc,
        "harmonic_accuracy": harmonic_acc,
        "train_samples": len(X_train),
        "test_samples": len(X_test),
        "feature_count": X.shape[1],
    }

    sample_df = pd.DataFrame(
        {
            "Actual Key": y_test.values[:15],
            "Predicted Key": y_pred[:15],
            "Harmonically Compatible": [
                y_pred[i] in get_camelot_neighbors(y_test.values[i])
                for i in range(min(15, len(y_test)))
            ],
        }
    )

    return model, metrics, sample_df
