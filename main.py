import pandas as pd

from src.video_processing import process_video
from src.training_data import create_training_data
from src.throw_classifier import train_throw_classifier
from src.analyze_throw import analyze_throw
from src.prediction_cleanup import prediction_cleanup
from joblib import load

MODEL_PATH = "models/pose_landmarker_full.task"
VIDEO_PATH_TEST = "data/raw_videos/jalen_hurts_throw.mp4"

throw_model = load("models/throw_classifier.joblib")
process_video(VIDEO_PATH_TEST, MODEL_PATH)

results, prediction_df = analyze_throw(VIDEO_PATH_TEST, MODEL_PATH, throw_model)

print(results)
print(prediction_df["prediction"].value_counts())
print(prediction_df[prediction_df["prediction"] == 1])

