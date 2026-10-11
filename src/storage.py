import os
from dotenv import load_dotenv
from supabase import create_client

load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(
    SUPABASE_URL, 
    SUPABASE_KEY
)

def upload_annotated_video(local_path, storage_path):
    with open(local_path, "rb") as video_file: 
        response=supabase.storage.from_("annotated-videos").upload(
            path=storage_path, 
            file=video_file, 
        )
        return response

    

def get_public_video_url(storage_path): 
    return supabase.storage.from_("annotated-videos").get_public_url(storage_path)