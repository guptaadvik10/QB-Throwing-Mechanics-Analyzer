import pandas as pd
from sklearn.inspection import permutation_importance

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
    "brees": "outputs/brees_angles.csv",
    "rodgers": "outputs/rodgers_angles.csv",
    "wilson": "outputs/wilson_angles.csv",
    "stroud": "outputs/stroud_angles.csv",
    "herbert": "outputs/herbert_angles.csv",
    "combine_1": "outputs/combine_1_angles.csv"
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

    perm_importance = permutation_importance(
        model, X_test, y_test, scoring="f1", n_repeats=10, random_state=4
    )

    for feature, importance in zip(X.columns, perm_importance.importances_mean):
         print(f"{feature}: {importance:.4f}")

         results.append(
            {
            "fold": fold,
            "feature": feature,
            "importance": importance
        }
         )

results_df = pd.DataFrame(results)
summary = (
    results_df.groupby("feature")["importance"]
    .agg(["mean", "std"])
    .sort_values("mean", ascending=False)
)

print(summary)