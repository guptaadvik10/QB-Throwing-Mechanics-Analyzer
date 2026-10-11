from joblib import dump
import pandas as pd
from src.throw_classifier import train_throw_classifier
from src.training_data import create_training_data

brady_df = pd.read_csv("outputs/brady_angles.csv")
allen_df = pd.read_csv("outputs/allen_angles.csv")
mahomes_df = pd.read_csv("outputs/mahomes_angles.csv")
hurts_df = pd.read_csv("outputs/hurts_angles.csv")
stafford_1_df = pd.read_csv("outputs/stafford_1_angles.csv")
stafford_2_df = pd.read_csv("outputs/stafford_2_angles.csv")
brees_df = pd.read_csv("outputs/brees_angles.csv")
rodgers_df = pd.read_csv("outputs/rodgers_angles.csv")
wilson_df = pd.read_csv("outputs/wilson_angles.csv")
stroud_df = pd.read_csv("outputs/stroud_angles.csv")
herbert_df = pd.read_csv("outputs/herbert_angles.csv")
combine_1_df = pd.read_csv("outputs/combine_1_angles.csv")


training_df = pd.concat(
    [allen_df, mahomes_df, stafford_1_df, rodgers_df, herbert_df, wilson_df, combine_1_df, stafford_2_df],
    ignore_index = True
)

X, y = create_training_data(training_df)
throw_model = train_throw_classifier(X, y)


dump(throw_model, "models/throw_classifier.joblib")