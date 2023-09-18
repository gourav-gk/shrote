import cv2
from ultralytics import YOLO
import pyttsx3
from face import recognize

# Load the YOLOv8 model
model = YOLO("yolov8n.pt")

# Initialize the text-to-speech engine
engine = pyttsx3.init()


def detect():
    # cap = cv2.VideoCapture(video_path)

    cap = cv2.VideoCapture(0)

    # Flag to indicate whether to capture a single frame
    capture_frame = False

    response = ""
    person =""
    object_counts = {}

    engine.say("Please wait for some time this may take a minute")
    engine.runAndWait()

    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:
            if not capture_frame:
                # Run YOLOv8 inference on the frame
                results = model(frame)

                # Visualize the results on the frame
                annotated_frame = results[0].plot()

                # Display the annotated frame
                cv2.imshow("YOLOv8 Inference", annotated_frame)

                if results[0].boxes:
                    for result in results[0].boxes:
                        obj = results[0].names[result.cls[0].item()]

                        if obj in object_counts:
                            object_counts[obj] += 1
                        else:
                            object_counts[obj] = 1

                    for obj, count in object_counts.items():
                        response = response+str(count)+" "+obj+", "


                    cv2.imwrite("detected_frame.jpg", frame)
                    capture_frame = True

                    cap.release()
                    cv2.destroyAllWindows()

                    if "person" in response:
                        faces = recognize()

                        for face in faces:
                            person = person + face + ", "

                        if len(faces) > 0:
                            person = " Which includes "+person[0:-2]


                    response = response[0:-2]+" detected."+person

                    return response


            if cv2.waitKey(1) & 0xFF == ord("q") or capture_frame:
                break
        else:
            # Break the loop if the end of the video is reached
            break

