import cv2
import os

def save_sample_frames(video_path, output_folder, frame_numbers):
    cap = cv2.VideoCapture(video_path)
    

    if not cap.isOpened():
        print("Could not open video")
        return
    
    fps = cap.get(cv2.CAP_PROP_FPS)
    os.makedirs(output_folder, exist_ok = True)

    for frame_number in frame_numbers:
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        ret, frame = cap.read()

        if ret: 
            timestamp = frame_number / fps
            label = f"frame: {frame_number}, timestamp: {timestamp:.2f}s"

            cv2.putText(
                frame, 
                label, 
                (50, 80), 
                cv2.FONT_HERSHEY_COMPLEX,
                2, (255, 255, 255), 4
            )

            output_path = os.path.join(output_folder, f"frame_{frame_number}.jpg")
            saved = cv2.imwrite(output_path, frame)

            if saved: 
                print(f"saved frame {frame_number}")
            else: 
                print(f"Could not save frame {frame_number}")

        else: 
            print(f"Could not read frame {frame_number}")
        

    cap.release()

