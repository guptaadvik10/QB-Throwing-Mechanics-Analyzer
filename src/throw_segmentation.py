import pandas as pd

def throw_segmentation(df: pd.DataFrame):
    df = df.copy()
    df["throw_phase"] = 0

    df["wrist_change"] = (
        df["wrist_x"].diff() **2
        + df["wrist_y"].diff() **2
    ) ** 0.5

    df.loc[df["wrist_change"] > 0.05, "throw_phase"] = 1
    return df

