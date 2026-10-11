import cv2


def frame_labeler(video_path):

    cap = cv2.VideoCapture(video_path)

    frame_number = 0

    while True:
        
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)

        ret, frame = cap.read()

        if not ret:
            break

        cv2.putText(
            frame, 
            f"Frame: {frame_number}", 
            (30, 50),
            cv2.FONT_HERSHEY_COMPLEX, 
            1, 
            (0, 255, 0), 
            2
        )

        cv2.imshow("Frame Labeler", frame)
        key = cv2.waitKey(0)

        if key == ord("d"):
            frame_number += 1
        elif key == ord("a"):
            frame_number = max(0, frame_number - 1)
        elif key == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()