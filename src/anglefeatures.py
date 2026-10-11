import math

def calculate_angle(a, b, c):
    angle_1 = math.atan2(
        a[1] - b[1],
        a[0] - b[0]
    )
    angle_2 = math.atan2(
        c[1] - b[1],
        c[0] - b[0]
    )
    angle = math.degrees(angle_2 - angle_1)
    angle = abs(angle)
    
    if angle > 180:
        angle = 360-angle 
    return angle
    

def upper_arm_direction(a, b):
    angle = math.atan2(
        b[1] - a[1], 
        b[0] - a[0]
    )

    angle = math.degrees(angle)

    return angle