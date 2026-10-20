import pandas as pd
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

from src.cross_validation import get_cv_splits
from src.training_data import create_training_data
from src.throw_classifier import train_throw_classifier

videos = {
    "brady": "outputs/brady_angles.csv",
    "allen": "outputs/allen_angles.csv",
    "mahomes": "outputs/mahomes_angles.csv",
    "hurts": "outputs/hurts_angles.csv",
    "stafford_1": "outputs/stafford_1_angles.csv",
    "stafford_2": "outputs/stafford_2_angles.csv",
    "rodgers": "outputs/rodgers_angles.csv",
    "wilson": "outputs/wilson_angles.csv",
    "stroud": "outputs/stroud_angles.csv",
    "herbert": "outputs/herbert_angles.csv",
    "combine_1": "outputs/combine_1_angles.csv", 
    "training_1_": "outputs/training_1_angles.csv",
    "kid_throw_1": "outputs/kid_throw_1_angles.csv", 
    "kurt_benkert_1": "outputs/kurt_benkert_1_angles.csv", 
    "kurt_benkert_2": "outputs/kurt_benkert_2_angles.csv",

}

dfs = []

for name, path in videos.items():
    df = pd.read_csv(path)
    df["video_id"] = name
    dfs.append(df)

full_df = pd.concat(dfs, ignore_index=True)

X, y = create_training_data(full_df)

results = []

for fold, (train_idx, test_idx) in enumerate(get_cv_splits(X, y, full_df["video_id"])):
    X_train, X_test = X.iloc[train_idx], X.iloc[test_idx]
    y_train, y_test = y.iloc[train_idx], y.iloc[test_idx]

    model = train_throw_classifier(X_train, y_train)

    y_pred = model.predict(X_test)

    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, zero_division=0)
    recall = recall_score(y_test, y_pred, zero_division=0)
    f1 = f1_score(y_test, y_pred, zero_division=0)

    print(f"Fold {fold+1} - Accuracy: {accuracy:.4f}, Precision: {precision:.4f}, Recall: {recall:.4f}, F1: {f1:.4f}")

    results.append(
        {
            "fold": fold+1,
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1
        }
    )

results_df = pd.DataFrame(results)
results_df.to_csv("results.csv", index=False)
print(results_df[["accuracy", "precision", "recall", "f1"]].mean())
