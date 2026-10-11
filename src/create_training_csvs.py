import pandas as pd
from sklearn.model_selection import StratifiedGroupKFold

from src.video_processing import process_video
from src.signal_cleaning import elbow_angle_cleaning
from src.throw_segmentation import throw_segmentation

MODEL_PATH = "models/pose_landmarker_full.task"


# VIDEO 1 TOM BRADY

brady_raw_df = process_video("data/raw_videos/tom_brady_throw.mp4", MODEL_PATH)
brady_raw_df = pd.DataFrame(brady_raw_df)
brady_cleaned_df = elbow_angle_cleaning(brady_raw_df)

brady_cleaned_df["throwing_label"] = 0
brady_cleaned_df.loc[
    (brady_cleaned_df["frame_number"] > 41) &
    (brady_cleaned_df["frame_number"] < 52), 
    "throwing_label"
] = 1
    
brady_cleaned_df.to_csv(
    "outputs/brady_angles.csv",
    index=False
)

# VIDEO 2 JOSH ALLEN

allen_raw_df = process_video("data/raw_videos/josh_allen_throw.mp4", MODEL_PATH)
allen_raw_df = pd.DataFrame(allen_raw_df)
allen_cleaned_df = elbow_angle_cleaning(allen_raw_df)

allen_cleaned_df["throwing_label"] = 0
allen_cleaned_df.loc[
    (allen_cleaned_df["frame_number"] > 45) &
    (allen_cleaned_df["frame_number"] < 58), 
    "throwing_label"
] = 1

    
allen_cleaned_df.to_csv(
    "outputs/allen_angles.csv",
    index=False
)


# VIDEO 3 PATRICK MAHOMES

mahomes_raw_df = process_video("data/raw_videos/patrick_mahomes_throw.mp4", MODEL_PATH)
mahomes_raw_df = pd.DataFrame(mahomes_raw_df)
mahomes_cleaned_df = elbow_angle_cleaning(mahomes_raw_df)

mahomes_cleaned_df["throwing_label"] = 0
mahomes_cleaned_df.loc[
    (mahomes_cleaned_df["frame_number"] > 64) &
    (mahomes_cleaned_df["frame_number"] < 78), 
    "throwing_label"
] = 1
    
mahomes_cleaned_df.to_csv(
    "outputs/mahomes_angles.csv",
    index=False
)



# VIDEO 4 JALEN HURTS

hurts_raw_df = process_video("data/raw_videos/jalen_hurts_throw.mp4", MODEL_PATH)
hurts_raw_df = pd.DataFrame(hurts_raw_df)
hurts_cleaned_df = elbow_angle_cleaning(hurts_raw_df)

hurts_cleaned_df["throwing_label"] = 0
hurts_cleaned_df.loc[
    (hurts_cleaned_df["frame_number"] > 16) &
    (hurts_cleaned_df["frame_number"] < 27), 
    "throwing_label"
] = 1
    
hurts_cleaned_df.to_csv(
    "outputs/hurts_angles.csv",
    index=False
)



# VIDEO 5 MATTHEW STAFFORD 1

stafford_1_raw_df = process_video("data/raw_videos/matthew_stafford_throw_1.mp4", MODEL_PATH)
stafford_1_raw_df = pd.DataFrame(stafford_1_raw_df)
stafford_1_cleaned_df = elbow_angle_cleaning(stafford_1_raw_df)

stafford_1_cleaned_df["throwing_label"] = 0
stafford_1_cleaned_df.loc[
    (stafford_1_cleaned_df["frame_number"] > 77) &
    (stafford_1_cleaned_df["frame_number"] < 88), 
    "throwing_label"
] = 1
    
stafford_1_cleaned_df.to_csv(
    "outputs/stafford_1_angles.csv",
    index=False
)


### VIDEO 6 MATTHEW STAFFORD 2

stafford_2_raw_df = process_video("data/raw_videos/matthew_stafford_throw_2.mp4", MODEL_PATH)
stafford_2_raw_df = pd.DataFrame(stafford_2_raw_df)
stafford_2_cleaned_df = elbow_angle_cleaning(stafford_2_raw_df)

stafford_2_cleaned_df["throwing_label"] = 0
stafford_2_cleaned_df.loc[
    (stafford_2_cleaned_df["frame_number"] > 13) &
    (stafford_2_cleaned_df["frame_number"] < 23), 
    "throwing_label"
] = 1
    
stafford_2_cleaned_df.to_csv(
    "outputs/stafford_2_angles.csv",
    index=False
)


### VIDEO 7 DREW BREES

brees_raw_df = process_video("data/raw_videos/drew_brees_throw.mp4", MODEL_PATH)
brees_raw_df = pd.DataFrame(brees_raw_df)
brees_cleaned_df = elbow_angle_cleaning(brees_raw_df)

brees_cleaned_df["throwing_label"] = 0
brees_cleaned_df.loc[
    (brees_cleaned_df["frame_number"] > 38) &
    (brees_cleaned_df["frame_number"] < 48), 
    "throwing_label"
] = 1
    
brees_cleaned_df.to_csv(
    "outputs/brees_angles.csv",
    index=False
)



rodgers_raw_df = process_video("data/raw_videos/aaron_rodgers_throw.mp4", MODEL_PATH)
rodgers_raw_df = pd.DataFrame(rodgers_raw_df)
rodgers_cleaned_df = elbow_angle_cleaning(rodgers_raw_df)

rodgers_cleaned_df["throwing_label"] = 0
rodgers_cleaned_df.loc[
    (rodgers_cleaned_df["frame_number"] > 58) &
    (rodgers_cleaned_df["frame_number"] < 68), 
    "throwing_label"
] = 1
    
rodgers_cleaned_df.to_csv(
    "outputs/rodgers_angles.csv",
    index=False
)


herbert_raw_df = process_video("data/raw_videos/justin_herbert_throw.mp4", MODEL_PATH)
herbert_raw_df = pd.DataFrame(herbert_raw_df)
herbert_cleaned_df = elbow_angle_cleaning(herbert_raw_df)

herbert_cleaned_df["throwing_label"] = 0
herbert_cleaned_df.loc[
    (herbert_cleaned_df["frame_number"] > 47) &
    (herbert_cleaned_df["frame_number"] < 61), 
    "throwing_label"
] = 1
    
herbert_cleaned_df.to_csv(
    "outputs/herbert_angles.csv",
    index=False
)


combine_1_raw_df = process_video("data/raw_videos/combine_throw_1.mp4", MODEL_PATH)
combine_1_raw_df = pd.DataFrame(combine_1_raw_df)
combine_1_cleaned_df = elbow_angle_cleaning(combine_1_raw_df)

combine_1_cleaned_df["throwing_label"] = 0
combine_1_cleaned_df.loc[
    (combine_1_cleaned_df["frame_number"] > 14) &
    (combine_1_cleaned_df["frame_number"] < 24), 
    "throwing_label"
] = 1
    
combine_1_cleaned_df.to_csv(
    "outputs/combine_1_angles.csv",
    index=False
)



stroud_raw_df = process_video("data/raw_videos/cj_stroud_throw.mp4", MODEL_PATH)
stroud_raw_df = pd.DataFrame(stroud_raw_df)
stroud_cleaned_df = elbow_angle_cleaning(stroud_raw_df)

stroud_cleaned_df["throwing_label"] = 0
stroud_cleaned_df.loc[
    (stroud_cleaned_df["frame_number"] > 49) &
    (stroud_cleaned_df["frame_number"] < 59), 
    "throwing_label"
] = 1
    
stroud_cleaned_df.to_csv(
    "outputs/stroud_angles.csv",
    index=False
)


wilson_raw_df = process_video("data/raw_videos/russel_wilson_throw.mp4", MODEL_PATH)
wilson_raw_df = pd.DataFrame(wilson_raw_df)
wilson_cleaned_df = elbow_angle_cleaning(wilson_raw_df)

wilson_cleaned_df["throwing_label"] = 0
wilson_cleaned_df.loc[
    (wilson_cleaned_df["frame_number"] > 75) &
    (wilson_cleaned_df["frame_number"] < 87), 
    "throwing_label"
] = 1
    
wilson_cleaned_df.to_csv(
    "outputs/wilson_angles.csv",
    index=False
)

