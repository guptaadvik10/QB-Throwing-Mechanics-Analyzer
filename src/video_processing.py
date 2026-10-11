import cv2
from src.anglefeatures import calculate_angle, upper_arm_direction
import mediapipe as mp

def process_video(video_path, model_path, display=True):
    BaseOptions = mp.tasks.BaseOptions
    PoseLandmarker_Options = mp.tasks.vision.PoseLandmarkerOptions
    PoseLandmarker = mp.tasks.vision.PoseLandmarker
    RunningMode = mp.tasks.vision.RunningMode

    base_options = BaseOptions(
        model_asset_path=model_path
    )

    options = PoseLandmarker_Options(
        base_options=base_options,
        running_mode = RunningMode.VIDEO
    )

    landmarker = PoseLandmarker.create_from_options(options)
    cap = cv2.VideoCapture(video_path)
    recorded_angles = []
    frame_number = 0

    while cap.isOpened():
        ret, frame = cap.read()

        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_frame = mp.Image(
            image_format = mp.ImageFormat.SRGB,
            data = rgb_frame
        )
        timestamp = int(cap.get(cv2.CAP_PROP_POS_MSEC))

        result = landmarker.detect_for_video(
            mp_frame, 
            timestamp
        )

        if result.pose_landmarks:
            main_pose = result.pose_landmarks[0]

            left_shoulder = main_pose[11]
            shoulder = main_pose[12]
            elbow = main_pose[14]
            wrist = main_pose[16]
            left_hip = main_pose[23]
            right_hip = main_pose[24]

            height, width = frame.shape[:2]

            shoulder_point = (
                int(shoulder.x * width), 
                int(shoulder.y * height)
            )

            left_shoulder_point = (
                int(left_shoulder.x * width), 
                int(left_shoulder.y * height)
            )
            elbow_point = (
                int(elbow.x * width), 
                int(elbow.y * height)
            )
            wrist_point = (
                int(wrist.x * width), 
                int(wrist.y * height)
            )
            

            elbow_angle = calculate_angle(shoulder_point, elbow_point, wrist_point)
            upper_arm_angle = upper_arm_direction(shoulder_point, elbow_point)

            frame_record = {
                "frame_number":  frame_number,
                "timestamp": timestamp, 
                "elbow_angle": elbow_angle,
                "upper_arm_angle": upper_arm_angle, 
                "shoulder_vis": shoulder.visibility, 
                "elbow_vis": elbow.visibility, 
                "wrist_vis": wrist.visibility,
                "elbow_x": elbow.x,
                "elbow_y": elbow.y,
                "wrist_x": wrist.x,
                "wrist_y": wrist.y,
                "shoulder_x": shoulder.x,
                "shoulder_y": shoulder.y,
                "left_shoulder_x": shoulder.x,
                "left_shoulder_y": shoulder.y,
                "left_hip_x": left_hip.x,
                "left_hip_y": left_hip.y,
                "right_hip_x": right_hip.x,
                "right_hip_y": right_hip.y,
            }

            recorded_angles.append(frame_record)

            if display: 
                cv2.circle(frame, shoulder_point, 15, (0, 255, 0), -1)
                cv2.circle(frame, elbow_point, 15, (0, 255, 0), -1)
                cv2.circle(frame, wrist_point, 15, (0, 255, 0), -1)

                cv2.line(frame, shoulder_point, elbow_point, (255, 255, 255), 4)
                cv2.line(frame, elbow_point, wrist_point, (255, 255, 255), 4)

                angle_text_point = (
                    elbow_point[0] + 40, elbow_point[1] + 25
                )
                cv2.putText(
                    frame, 
                    f"{elbow_angle}", 
                    angle_text_point, 
                    cv2.FONT_HERSHEY_COMPLEX, 
                    1, 
                    (0, 255, 255), 
                    4
                )
                cv2.putText(
                    frame, 
                    f"{timestamp}", 
                    (10, 30), 
                    cv2.FONT_HERSHEY_COMPLEX, 
                    1, 
                    (0, 255, 0), 
                    4
                )
                cv2.putText(
                    frame, 
                    f"{frame_number}", 
                    (10, 55), 
                    cv2.FONT_HERSHEY_COMPLEX, 
                    1, 
                    (0, 255, 0), 
                    4
                )

                cv2.imshow("frame", frame)
                key = cv2.waitKey(25)

                if key & 0xFF == ord('q'):
                    break

        frame_number +=1 
    cap.release()
    cv2.destroyAllWindows()

    return recorded_angles








