
import pandas as pd

TEMPORAL_FEATURES = [
    "wrist_change_mean_5",
    "wrist_change_max_5",
    "elbow_angle_delta_5",
    "elbow_height_delta_5",
]



def add_temporal_features(df):
    df = df.copy()

    # Sort by frame number if available
    if "frame_idx" in df.columns:
        df = df.sort_values("frame_idx")

    df["wrist_change_mean_5"] = (
        df["wrist_change"]
        .rolling(5, min_periods=1)
        .mean()
    )

    df["wrist_change_max_5"] = (
        df["wrist_change"]
        .rolling(5, min_periods=1)
        .max()
    )

    df["elbow_angle_delta_5"] = (
        df["elbow_angle_smoothed"]
        - df["elbow_angle_smoothed"].shift(5)
    )

    df["elbow_height_delta_5"] = (
        df["elbow_height"]
        - df["elbow_height"].shift(5)
    )

    df[
        ["elbow_angle_delta_5", "elbow_height_delta_5"]
    ] = df[
        ["elbow_angle_delta_5", "elbow_height_delta_5"]
    ].fillna(0)

    return df
