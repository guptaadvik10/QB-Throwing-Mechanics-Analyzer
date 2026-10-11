import pandas as pd

def prediction_cleanup(df, min_run_length = 5):

    for frame in range(1, len(df) - 1):
        if (
            df.loc[frame-1, "prediction"] == 1 and
            df.loc[frame, "prediction"] == 0 and
            df.loc[frame + 1, "prediction"] == 1
        ):
            df.loc[frame, "prediction"] = 1
        elif(
            df.loc[frame - 1, "prediction"] == 1
            and df.loc[frame, "prediction"] == 0
            and df.loc[frame + 1, "prediction"] == 0
            and df.loc[frame + 2, "prediction"] == 1
        ):
            df.loc[frame, "prediction"] = 1
            df.loc[frame + 1, "prediction"] = 1
   
    run_length = 0
    run_start = None
   
    for frame in range(len(df)):
        if df.loc[frame, "prediction"] == 1:
            
            if run_length == 0:
                run_start = frame

            run_length += 1

        else:
            if run_length > 0:
                print(run_start, run_length)

                if run_length < min_run_length:
                    df.loc[run_start: frame-1, "prediction"] = 0

            run_start = None
            run_length = 0

    
    if run_length > 0 and run_length < min_run_length:
        print(run_start, run_length)
        df.loc[
            run_start:len(df) - 1,
            "prediction"
        ] = 0

    return df


