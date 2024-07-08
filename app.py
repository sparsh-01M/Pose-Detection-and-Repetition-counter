from flask import Flask, request, render_template
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def count_reps(video_path):
    import cv2
    import mediapipe as mp

    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    cap = cv2.VideoCapture(video_path)
    count = 0
    threshold = 0.5  # Example threshold for pose detection
    previous_pose = None

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = pose.process(image)

        if results.pose_landmarks:
            landmarks = results.pose_landmarks.landmark
            # Add your logic for counting repetitions based on landmarks
            current_pose = landmarks[mp_pose.PoseLandmark.NOSE].visibility
            if previous_pose is not None and current_pose > threshold and previous_pose < threshold:
                count += 1
            previous_pose = current_pose

    cap.release()
    return count

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'
    file = request.files['file']
    if file.filename == '':
        return 'No selected file'
    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        reps_count = count_reps(file_path)
        return f'Repetitions counted: {reps_count}'

if __name__ == '__main__':
    app.run(debug=True)
