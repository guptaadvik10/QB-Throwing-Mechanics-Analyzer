
features = [
        "wrist_change",
        "arm_visibility",
        "wrist_to_shoulder_2", 
        "shoulder_rotation_change"
    ]

def create_features(df):
    X = df[features]
    return X

def create_training_data(df):
    X = df[features]
    y = df["throwing_label"]

    return X, y