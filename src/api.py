from fastapi import FastAPI, UploadFile, File
import tempfile
from joblib import load
from src.analyze_throw import analyze_throw
from fastapi.middleware.cors import CORSMiddleware
from src.video_annotation import create_annotated_video
from fastapi.staticfiles import StaticFiles 

from src.database import Base, engine, SessionLocal
from src import models
from src.models import Analysis
import uuid
from src.storage import upload_annotated_video, get_public_video_url

from src.compare_metrics import compare_metrics


Base.metadata.create_all(bind=engine)

app = FastAPI()

app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8081"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL_PATH = "models/pose_landmarker_full.task"
throw_model = load("models/throw_classifier.joblib")

@app.post("/analyze")
async def analyze_video(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete = False, suffix = ".mp4") as temp_file:
        contents = await file.read()
        temp_file.write(contents)

        temp_path = temp_file.name

        metrics, analysis_df, coach_analysis = analyze_throw(
            temp_path, 
            MODEL_PATH, 
            throw_model
        )

        output_path = "outputs/annotated_throw.mp4"

        create_annotated_video(
            temp_path,
            output_path,
            analysis_df
        )

        video_id = str(uuid.uuid4())
        storage_path = f"analyses/{video_id}.mp4"

        upload_annotated_video(output_path, storage_path)
        public_url = get_public_video_url(storage_path)


        throw_frames = analysis_df.loc[
            analysis_df["prediction"] == 1,
            ["frame_number", "prediction"]
        ].to_dict(orient="records")

        db = SessionLocal()
        new_analysis = Analysis(
            video_name=file.filename,
            annotated_video_url=public_url,
            min_elbow_angle=metrics["min_elbow_angle"],
            max_elbow_angle=metrics["max_elbow_angle"],
            arm_slot=metrics["arm_slot"],
            elbow_rom=metrics["elbow_rom"],
            torso_tilt=metrics["torso_tilt"],
            shoulder_abduction=metrics["shoulder_abduction"],
            elbow_height=metrics["elbow_height"],
            release_velocity=metrics["release_velocity"],
            throw_series=metrics["throw_series"]
        )
        db.add(new_analysis)
        db.commit()
        db.refresh(new_analysis)
        db.close()

        return {
            "metrics": metrics, 
            "throw_frames": throw_frames,
            "annotated_video_url": "http://localhost:8000/outputs/annotated_throw.mp4",
            "coach_analysis": coach_analysis

        }

@app.get("/analyses")
def get_analyses():

    db = SessionLocal()

    analyses = (
        db.query(Analysis)
        .order_by(Analysis.created_at.desc())
        .limit(5)
        .all()
    )

    db.close()

    return analyses



@app.get("/compare/{analysis_a_id}/{analysis_b_id}")
def compare_analyses(analysis_a_id: int, analysis_b_id: int): 

    db= SessionLocal()

    analysis_a = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_a_id)
        .first()
    )

    analysis_b = (
        db.query(Analysis)
        .filter(Analysis.id == analysis_b_id)
        .first()
    )

    metrics_a = {
        "arm_slot": analysis_a.arm_slot,
        "shoulder_abduction": analysis_a.shoulder_abduction,
        "elbow_height": analysis_a.elbow_height,
        "torso_tilt": analysis_a.torso_tilt,
        "elbow_rom": analysis_a.elbow_rom,
        "release_velocity": analysis_a.release_velocity,
    }

    metrics_b = {
        "arm_slot": analysis_b.arm_slot,
        "shoulder_abduction": analysis_b.shoulder_abduction,
        "elbow_height": analysis_b.elbow_height,
        "torso_tilt": analysis_b.torso_tilt,
        "elbow_rom": analysis_b.elbow_rom,
        "release_velocity": analysis_b.release_velocity,
    }

    comparision = compare_metrics(
        metrics_a, 
        metrics_b
    )

    db.close()
    
    return {
        "throw_a": {
            "id": analysis_a.id,
            "video_name": analysis_a.video_name,
            "annotated_video_url": analysis_a.annotated_video_url,
            "metrics": metrics_a,
            "throw_series": analysis_a.throw_series,
        },

        "throw_b": {
            "id": analysis_b.id,
            "video_name": analysis_b.video_name,
            "annotated_video_url": analysis_b.annotated_video_url,
            "metrics": metrics_b,
            "throw_series": analysis_b.throw_series,
        },

        "comparison": comparision
    }
