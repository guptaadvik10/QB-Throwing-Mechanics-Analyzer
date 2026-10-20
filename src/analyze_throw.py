from numpy import true_divide
import pandas as pd
import numpy as np

from src.video_processing import process_video
from src.signal_cleaning import elbow_angle_cleaning
from src.throw_segmentation import throw_segmentation
from src.training_data import create_features
from src.throw_metrics import throw_metrics
from src.prediction_cleanup import prediction_cleanup
from src.throw_summary import generate_throw_summary

def analyze_throw(video_path, model_path, throw_model):
    
    recorded_angles = process_video(video_path, model_path, display = False)

    df = pd.DataFrame(recorded_angles)    
    df = elbow_angle_cleaning(df)
    
    X_new = create_features(df)
    df["prediction"] = throw_model.predict(X_new)

    df = prediction_cleanup(df)

    prediction_df = df[["frame_number", "prediction"]].copy()

    throw_df = df[df["prediction"] == 1].copy() 
    throw_df = throw_df.dropna(subset = ["elbow_angle_smoothed"])

    if throw_df.empty: 
        return {"throw_detected": False}, df, None

    throw_df["standardized"] = np.linspace(0, 100, len(throw_df))

    throw_series = (
        throw_df[["standardized", "elbow_angle_smoothed"]]
        .to_dict(orient = "records")
    )

    df["prediction"] = prediction_df["prediction"]

    min_elbow_angle, max_elbow_angle, elbow_rom, max_frame, release_velocity, shoulder_abduction, elbow_height, torso_tilt, arm_slot, arm_slot_class= throw_metrics(throw_df)

    print("finished mechanics")

    metrics = {
        "throw_detected": True,
        "min_elbow_angle": float(min_elbow_angle),
        "max_elbow_angle": float(max_elbow_angle),
        "elbow_rom": float(elbow_rom), 
        "max_frame": int(max_frame), 
        "release_velocity": (
            None if pd.isna(release_velocity) else float(release_velocity)
        ),
        "shoulder_abduction": float(shoulder_abduction), 
        "elbow_height": float(elbow_height),
        "torso_tilt": float(torso_tilt), 
        "arm_slot": float(arm_slot),
        "arm_slot_class": str(arm_slot_class), 

        "throw_series": throw_series
    }
    print("calling OpenAI...")
    print(metrics["throw_series"][:5])

    coach_analysis = generate_throw_summary(metrics)
    print("OpenAI finished")

    return metrics, df, coach_analysis



