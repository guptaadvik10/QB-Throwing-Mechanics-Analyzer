import matplotlib.pyplot as plt

def raw_vs_clean(df):
    plt.plot(
        df["timestamp"], 
        df["elbow_angle"], 
        label="Raw Angle"
    )
    plt.plot(
        df["timestamp"], 
        df["elbow_angle_clean"], 
        label="Clean Angle"
    )
    plt.xlabel("Time (ms)")
    plt.ylabel("Elbow Angle")
    plt.legend()
    plt.show()
    
def clean_vs_interpolated(df):
    plt.plot(
        df["timestamp"], 
        df["elbow_angle_clean"], 
        label="Clean Angle"
    )
    plt.plot(
        df["timestamp"], 
        df["elbow_angle_interpolated"], 
        label="Interpolated Angle"
    )
    plt.xlabel("Time (ms)")
    plt.ylabel("Elbow Angle")
    plt.legend()
    plt.show()

def interpolated_vs_smoothed(df):
    plt.plot(
        df["timestamp"], 
        df["elbow_angle_interpolated"], 
        label="Interpolated Angle"
    )
    plt.plot(
        df["timestamp"], 
        df["elbow_angle_smoothed"], 
        label="Smoothed Angle"
    )
    plt.xlabel("Time (ms)")
    plt.ylabel("Elbow Angle")
    plt.legend()
    plt.show()

def throw_phase_vs_wrist(df):
    plt.plot(
        df["timestamp"],
        df["wrist_change"],
        label="Wrist Change"
    )
   
    plt.xlabel("Time (ms)")
    plt.ylabel("Wrist Change and Throw Phase")
    plt.legend()
    plt.show()