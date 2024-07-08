# Pose-Detection-and-Repetition-counter


# Pose-Detection-for-Repetitions-Counter

Our project uses Mediapipe for real-time pose estimation and OpenCV for video capture to accurately count exercise repetitions. It tracks key body landmarks, analyzes movement patterns, and provides instant feedback to ensure proper form. Adaptable for various exercises, it enhances fitness tracking and reduces injury risk.

## Features

- **Real-time Pose Estimation**: Utilizes Mediapipe for detecting and tracking key body landmarks in real-time.
- **Exercise Repetition Counting**: Analyzes movement patterns to accurately count exercise repetitions.
- **Form Feedback**: Provides instant feedback to ensure proper exercise form.
- **Adaptable for Various Exercises**: Supports a wide range of exercises with different movement patterns.
- **Injury Risk Reduction**: Helps in maintaining proper form to reduce the risk of injuries.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/Pose-Detection-for-Repetitions-Counter.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Pose-Detection-for-Repetitions-Counter
    ```
3. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. Run the script:
    ```bash
    python main.py
    ```
2. The webcam feed will open. Perform the exercise in front of the camera.
3. The program will track your movements, count repetitions, and display the count on the screen.
4. Press 'q' to quit the webcam feed.

## Code Explanation

### Importing Libraries

```python
import cv2
import mediapipe as mp
import numpy as np
```

### Setup Mediapipe and OpenCV

```python
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

cap = cv2.VideoCapture(0)
```

### Function to Calculate Angles

```python
def calculate_angle(a, b, c):
    a = np.array(a)
    b = np.array(b)
    c = np.array(c)
    
    radians = np.arctan2(c[1] - b[1], c[0] - b[0]) - np.arctan2(a[1] - b[1], a[0] - b[0])
    angle = np.abs(radians * 180.0 / np.pi)
    
    if angle > 180.0:
        angle = 360 - angle
        
    return angle
```

### Main Loop for Pose Detection and Repetition Counting

```python
counter = 0
stage = None

with mp_pose.Pose(min_detection_confidence=0.5, min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        ret, frame = cap.read()
        
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        
        results = pose.process(image)
        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        
        try:
            landmarks = results.pose_landmarks.landmark
            
            shoulder = [landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].x,
                        landmarks[mp_pose.PoseLandmark.LEFT_SHOULDER.value].y]
            elbow = [landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_ELBOW.value].y]
            wrist = [landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].x,
                     landmarks[mp_pose.PoseLandmark.LEFT_WRIST.value].y]
            
            angle = calculate_angle(shoulder, elbow, wrist)
            
            cv2.putText(image, str(angle), 
                        tuple(np.multiply(elbow, [640, 480]).astype(int)), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2, cv2.LINE_AA)
            
            if angle > 160:
                stage = "down"
            if angle < 30 and stage == 'down':
                stage = "up"
                counter += 1
                print(counter)
                       
        except:
            pass
        
        cv2.rectangle(image, (0, 0), (225, 73), (245, 117, 16), -1)
        
        cv2.putText(image, 'REPS', (15, 12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, str(counter), 
                    (10, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        
        cv2.putText(image, 'STAGE', (65, 12), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1, cv2.LINE_AA)
        cv2.putText(image, stage, 
                    (60, 60), 
                    cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255), 2, cv2.LINE_AA)
        
        mp_drawing.draw_landmarks(image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                                  mp_drawing.DrawingSpec(color=(245, 117, 66), thickness=2, circle_radius=2), 
                                  mp_drawing.DrawingSpec(color=(245, 66, 230), thickness=2, circle_radius=2))
        
        cv2.imshow('Mediapipe Feed', image)
        
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
```

## Contributing

We welcome contributions to this project. Please feel free to submit a pull request or open an issue if you have any suggestions or bug reports.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.

## Acknowledgements

- [Mediapipe](https://github.com/google/mediapipe) by Google
- [OpenCV](https://opencv.org/)
