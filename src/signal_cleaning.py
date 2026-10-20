import pandas as pd
import numpy as np

def elbow_angle_cleaning(df: pd.DataFrame, visibility_threshold: float = 0.5, max_angle_change: float = 45, max_interpolation_gap: int=2, max_smoothing_window: int=3, 
    max_shoulder_jump: float=60, max_elbow_jump: float=80, max_wrist_jump: float=120, max_bone_length_change: float=0.20):
    

    cleaned_angle = df.copy()

    ### UPPER ARM AND FOREARM LENTH CALCULATIONS

    cleaned_angle = landmark_motion(cleaned_angle, "shoulder")
    cleaned_angle = landmark_motion(cleaned_angle, "elbow")
    cleaned_angle = landmark_motion(cleaned_angle, "wrist")

    cleaned_angle["upper_arm_length"] = np.sqrt(
    (cleaned_angle["shoulder_x"] - cleaned_angle["elbow_x"]) ** 2 +
    (cleaned_angle["shoulder_y"] - cleaned_angle["elbow_y"]) ** 2)

    cleaned_angle["forearm_length"] = np.sqrt(
    (cleaned_angle["elbow_x"] - cleaned_angle["wrist_x"]) ** 2 +
    (cleaned_angle["elbow_y"] - cleaned_angle["wrist_y"]) ** 2)

    cleaned_angle["upper_arm_length_change"] = cleaned_angle["upper_arm_length"].pct_change().abs()
    cleaned_angle["forearm_length_change"] = cleaned_angle["forearm_length"].pct_change().abs()


    ### CLEANING ELBOW ANGLE

    cleaned_angle["angle_change"] = (cleaned_angle["elbow_angle"].diff())

    cleaned_angle["trust"] = (
        (cleaned_angle["shoulder_vis"] > visibility_threshold) &
        (cleaned_angle["elbow_vis"] > visibility_threshold) &
        (cleaned_angle["wrist_vis"] > visibility_threshold) &
        (cleaned_angle["angle_change"].abs() < max_angle_change) 
    )

    cleaned_angle["elbow_angle_clean"] = (cleaned_angle["elbow_angle"].where(cleaned_angle["trust"]))

    #### BUILDING INTERPOLATION TOOLS

    cleaned_angle["angle_missing"] = (cleaned_angle["elbow_angle_clean"].isna())
    
    cleaned_angle["new_group"] = (
        cleaned_angle["angle_missing"].shift() != cleaned_angle["angle_missing"]
    )
    cleaned_angle["gap_group"] = cleaned_angle["new_group"].cumsum()

    missing_rows = cleaned_angle[cleaned_angle["angle_missing"]]
    missing_gap_sizes = (
        missing_rows
        .groupby(cleaned_angle["gap_group"])
        .size()
    )

    short_gap_groups = missing_gap_sizes[missing_gap_sizes <= max_interpolation_gap].index
    interpolated_angles = (cleaned_angle["elbow_angle_clean"].interpolate())
    
    short_gap_filter = (
        cleaned_angle["angle_missing"] & 
        cleaned_angle["gap_group"].isin(short_gap_groups)
    )
    cleaned_angle["elbow_angle_interpolated"] = (
        cleaned_angle["elbow_angle_clean"].mask( 
            short_gap_filter, 
            interpolated_angles
        )
    )

    ### SMOOTHING ANGLE

    cleaned_angle["elbow_angle_smoothed"] = (
        cleaned_angle["elbow_angle_interpolated"]
        .rolling(
            window = max_smoothing_window,
            center = True
        )
        .mean()
    )

    ### Elbow angular velocity calculation

    cleaned_angle["elbow_angular_velocity"] = (
        cleaned_angle["elbow_angle_smoothed"]
        - cleaned_angle["elbow_angle_smoothed"].shift(2)
    ) / (
        (cleaned_angle["timestamp"]
        - cleaned_angle["timestamp"].shift(2)) / 1000
    )

    ### WRIST SHOULDER STATISTICS FOR THROW INTERVAL MODEL

    cleaned_angle["wrist_change"] = (
        cleaned_angle["wrist_x"].diff() ** 2 
        + cleaned_angle["wrist_y"].diff() ** 2
    ) ** 0.5

    cleaned_angle["wrist_shoulder_diff"] = cleaned_angle["shoulder_y"] - cleaned_angle["wrist_y"]
    cleaned_angle["wrist_to_shoulder"] = (cleaned_angle["shoulder_y"] - cleaned_angle["wrist_y"]) / abs(cleaned_angle["left_shoulder_x"] - cleaned_angle["shoulder_x"])

    cleaned_angle["shoulder_rotation"] = np.degrees(
        np.arctan2(
            cleaned_angle["shoulder_y"] - cleaned_angle["left_shoulder_y"], 
            cleaned_angle["shoulder_x"] - cleaned_angle["left_shoulder_x"], 

        )
    )
    cleaned_angle["shoulder_rotation"] =  cleaned_angle["shoulder_rotation"].replace(0, np.nan)
    cleaned_angle["shoulder_rotation_change"] = cleaned_angle["shoulder_rotation"].diff()

   
    cleaned_angle["wrist_to_shoulder_2"] = (cleaned_angle["shoulder_y"] - cleaned_angle["wrist_y"]) / cleaned_angle["upper_arm_length"]

    ### ARM VISIBILITY 

    cleaned_angle["arm_visibility"] = (
       df["shoulder_vis"] +
       df["elbow_vis"] +
       df["wrist_vis"]
   ) / 3

    cleaned_angle = arm_slot(cleaned_angle)
    cleaned_angle = shoulder_abduction(cleaned_angle)

    cleaned_angle["elbow_height"] = (
        cleaned_angle["shoulder_y"] - df["elbow_y"] 
    ) / cleaned_angle["upper_arm_length"]

    return cleaned_angle





def clean_upper_arm_angle(df):
    cleaned = df.copy()

    cleaned["upper_arm_angle_smoothed"] = (
        cleaned["upper_arm_angle"]
        .rolling(window=3, center=True)
        .mean()
    )

    return cleaned

def landmark_motion(df, name):
    df[f"{name}_dx"] = df[f"{name}_x"].diff()
    df[f"{name}_dy"] = df[f"{name}_y"].diff()

    df[f"{name}_speed_px"] = np.sqrt(
        df[f"{name}_dx"] **2 + 
        df[f"{name}_dy"] **2
    )

    return df




def shoulder_abduction(df):

    df = df.copy()

    shoulder_mid_x = (
        df["left_shoulder_x"] + df["shoulder_x"]
    ) / 2

    shoulder_mid_y = (
        df["left_shoulder_y"] + df["shoulder_y"]
    ) / 2

    hip_mid_x = (
        df["left_hip_x"] + df["right_hip_x"]
    ) / 2

    hip_mid_y = (
        df["left_hip_y"] + df["right_hip_y"]
    ) / 2

    torso_dx = hip_mid_x - shoulder_mid_x
    torso_dy = hip_mid_y - shoulder_mid_y
    
    arm_dx = df["elbow_x"]- df["shoulder_x"]
    arm_dy = df["elbow_y"] - df["shoulder_y"]

    dot = torso_dx * arm_dx + torso_dy * arm_dy

    torso_mag = np.sqrt(torso_dx**2 + torso_dy**2)
    arm_mag = np.sqrt(arm_dx**2 + arm_dy**2)

    cos_angle = dot / (torso_mag * arm_mag)
    cos_angle = np.clip(cos_angle, -1, 1)

    shoulder_abduction = np.degrees(np.arccos(cos_angle))

    df["shoulder_abduction"] = shoulder_abduction


    torso_mag = np.sqrt(
        torso_dx**2 + 
        torso_dy **2
    )

    cos_lean = np.clip(torso_dy / torso_mag, -1, 1)
    df["torso_lean"] = np.degrees(
        np.arccos(cos_lean)
    )

    return df


def arm_slot(df):
    arm_dx = df["wrist_x"]- df["shoulder_x"]
    arm_dy = df["wrist_y"] - df["shoulder_y"]

    arm_mag = np.sqrt(arm_dx**2 + arm_dy**2)

    dot_slot = arm_dx*0 + arm_dy *-1
    cos_angle_slot = dot_slot/(arm_mag)
    cos_angle_slot = np.clip(cos_angle_slot, -1, 1)
    
    arm_slot = np.degrees(np.arccos(cos_angle_slot))
    df["arm_slot"] = arm_slot

    return df



