from src.throw_summary import generate_throw_summary

metrics={
     "max_elbow_angle": 136.9,
    "min_elbow_angle": 37.1,
    "elbow_rom": 99.8,
    "elbow_velocity": 690.0,
    "shoulder_abduction": 117.4,
    "elbow_height": 0.7,
    "torso_tilt": 3.5,
    "arm_slot": 34.6,
    "arm_slot_class": "Three Quarters"
}

result = generate_throw_summary(metrics)
print(result)
