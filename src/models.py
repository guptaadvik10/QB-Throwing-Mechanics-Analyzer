from datetime import datetime
from sqlalchemy import Column, DateTime, Float, Integer, String
from src.database import Base
from sqlalchemy.dialects.postgresql import JSONB

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(Integer, primary_key = True, index=True)

    created_at = Column(
        DateTime, 
        default = datetime.utcnow
    )

    ### Video Info

    video_name = Column(String, nullable=True)
    annotated_video_url = Column(String, nullable=True)

     ### Metrics

    min_elbow_angle = Column(Float, nullable=True)
    max_elbow_angle = Column(Float, nullable=True)
    arm_slot = Column(Float, nullable=True)
    elbow_rom = Column(Float, nullable=True)
    torso_tilt = Column(Float, nullable=True)
    shoulder_abduction = Column(Float, nullable=True)
    elbow_height = Column(Float, nullable=True)
    release_velocity = Column(Float, nullable=True)
    throw_series = Column(JSONB, nullable=True)
   

