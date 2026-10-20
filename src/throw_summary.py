import json
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

def generate_throw_summary(metrics):

    prompt = f"""

    You are analyzing quarterback throwing mechanics. 

    Here are the emasured metrics: 

    Max elbow angle: {metrics["max_elbow_angle"]} degrees
    Min elbow angle: {metrics["min_elbow_angle"]} degrees
    Elbow range of motion: {metrics["elbow_rom"]} degrees
    Elbow velocity: {metrics["release_velocity"]} degrees/second
    Shoulder abduction: {metrics["shoulder_abduction"]} degrees
    Elbow height: {metrics["elbow_height"]}
    Torso tilt: {metrics["torso_tilt"]} degrees
    Arm slot: {metrics["arm_slot"]} degrees
    Arm slot classification: {metrics["arm_slot_class"]}

    Give a concise quarterback mechanic analysis

    Analyze these mechanics like a quarterback mechanics coach.

    Focus on:
    - what the throwing style looks like
    - how the metrics relate to each other
    - what characteristics stand out
    - what would be useful to track over repeated throws

    Do not simply repeat the numbers.
    Do not invent measurements.
    Do not diagnose injury risk.
    Do not claim a mechanic is good or bad unless the data clearly supports it.
    If there is not enough information to make a strong conclusion, say so.

    Return valid JSON with exactly this structure:

    {{
        "summary": "2-3 sentence mechanics interpretation",
        "strengths": ["meaningful observation 1", "meaningful observation 2"],
        "things_to_watch": ["meaningful observation 1", "meaningful observation 2"]
    }}
    """ 

    response = client.responses.create(
        model="gpt-5.6-luna", 
        input=prompt
    )

    return json.loads(response.output_text)