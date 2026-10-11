import pandas as pd
from src.video_processing import process_video
from src.signal_cleaning import elbow_angle_cleaning, clean_upper_arm_angle
from src.frame_labeler import frame_labeler
from src.video_annotation import create_annotated_video

VIDEO_PATH_TEST = "data/raw_videos/josh_allen_throw.mp4"
MODEL_PATH = "models/pose_landmarker_full.task"

df = process_video(VIDEO_PATH_TEST, MODEL_PATH)
df = pd.DataFrame(df)
print(df["shoulder_x"].head(5))