import cv2
import pandas as pd

def create_annotated_video(video_path, output_path, df):
    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"avc1")


    target_ratio = 9/16
    target_w = int(height * target_ratio)

    left = (width-target_w) // 2
    right = left + target_w

    writer = cv2.VideoWriter(
        output_path, 
        fourcc, 
        fps, 
        (target_w, height)
    )

    frame_number = 0

    while True: 
        ret, frame = cap.read()
        
        if not ret: 
            break
        
        frame = frame[:, left:right]

        matching_rows = df[df["frame_number"] == frame_number]

        if matching_rows.empty:
            writer.write(frame)
            frame_number += 1
            continue

        row = matching_rows.iloc[0]

        shoulder_x = int(row["shoulder_x"]*width) - left
        shoulder_y = int(row["shoulder_y"]*height)
        elbow_x = int(row["elbow_x"]*width) - left
        elbow_y = int(row["elbow_y"]*height)
        wrist_x = int(row["wrist_x"]*width) - left
        wrist_y = int(row["wrist_y"]*height)

        cv2.circle(frame, (shoulder_x, shoulder_y), 10, (0, 255, 0), 2)
        cv2.circle(frame, (wrist_x, wrist_y), 10, (0, 255, 0), 2)
        cv2.circle(frame, (elbow_x, elbow_y), 10, (0, 255, 0), 2)
        cv2.line(frame, (shoulder_x, shoulder_y), (elbow_x, elbow_y), (0, 0, 255, 2))
        cv2.line(frame, (wrist_x, wrist_y), (elbow_x, elbow_y), (0, 0, 255, 2))

        elbow_angle = row["elbow_angle_smoothed"]

        if pd.notna(elbow_angle):
            cv2.putText(
                frame, 
                f"Elbow Angle: {elbow_angle:.1f}",
                (30, 50),
                cv2.FONT_HERSHEY_COMPLEX, 
                1, 
                (0, 255, 0), 
                2
            )

        if row["prediction"] == 1:
            cv2.rectangle(frame, (0, 0), (width -1, height-1), (203, 204, 255), 5)


        writer.write(frame)
        frame_number += 1

    print("Frames written: ", frame_number)
    
    cap.release()
    writer.release()