from src.temporal_files import add_temporal_features

features = [
   "wrist_change",
    "wrist_to_shoulder_2",
    "elbow_angle_smoothed",
    "shoulder_rotation",
    "arm_slot",
    "torso_lean",
    "elbow_speed_px",
    "wrist_change_mean_5", 
    "wrist_change_max_5",
    "elbow_angle_delta_5", 
    "elbow_height_delta_5", 
    "elbow_height"
    ]

def create_features(df):
    df = add_temporal_features(df)
    X = df[features]
    return X

def create_training_data(df):
    X = df[features]
    y = df["throwing_label"]

    return X, y