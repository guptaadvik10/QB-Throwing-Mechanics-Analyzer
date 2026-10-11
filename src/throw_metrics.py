def throw_metrics(df):
    min_elbow_angle = df["elbow_angle_smoothed"].min()
    max_elbow_angle = df["elbow_angle_smoothed"].max()
    elbow_rom = max_elbow_angle - min_elbow_angle

    max_index = df["elbow_angle_smoothed"].idxmax()
    max_frame = df.loc[
        max_index, 
        "frame_number"
    ]

    df = df.copy()
    df["elbow_velocity"] = (
        df["elbow_angle_smoothed"]
        - df["elbow_angle_smoothed"].shift(2)
    ) / (
        (df["timestamp"]
        - df["timestamp"].shift(2)) / 1000
    )

    release_velocity = df.loc[
        max_index,
        "elbow_velocity"
    ]

    release_frame = df["wrist_change"].abs().idxmax()

    shoulder_abduction = df.loc[
        release_frame-2:release_frame+2,
        "shoulder_abduction"
    ].median()

    elbow_height = df.loc[
        release_frame, 
        "elbow_height"
    ]

    torso_tilt = df.loc[
        release_frame, 
        "torso_lean"
    ]
    arm_slot = df.loc[
        release_frame, 
        "arm_slot"
    ]

    if arm_slot > 0 and arm_slot < 20: 
        arm_slot_class = "Over the Top"
    elif arm_slot > 20 and arm_slot <= 60: 
        arm_slot_class = "Three Quarters"
    elif arm_slot > 60 and arm_slot <= 90: 
        arm_slot_class = "Sidearm"
    else:
        arm_slot_class="None"


    return min_elbow_angle, max_elbow_angle, elbow_rom, max_frame, release_velocity, shoulder_abduction, elbow_height, torso_tilt, arm_slot, arm_slot_class