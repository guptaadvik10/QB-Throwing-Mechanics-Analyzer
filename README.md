# QB Throwing Mechanics Analyzer

## Project Overview

An application that analyzes user-selected videos of quarterback throwing motions to provide biomechanical measurements and coaching feedback. Using computer vision and machine learning, the application tracks body movements, identifies throwing frames, and calculates key metrics such as arm slot, elbow height, and torso tilt. These results are used to provide insight into a developing quarterback's throwing mechanics and highlight potential areas for improvement.

## ✨ Feautures

- 🎥 **Video Based Throwing Analysis**: Extracts body poses and landmarks through MediaPipe Pose Detection
- 🤖 **Machine Learning Throw Detection**: Identifies throwing frame using Random Forest Classifier using extracted throw characteristics
- ☁️ **Cloud Database**: Automatic user storage using Supabase (PostgreSQL)
- ⚖️ **Throw Comparison**: Compare two throws side by side to examine differences
- 🧠 **AI Generated Coaching Feedback**: Summary of metrics in a digestible manner along with key insights
- 📱 **Interactive Application**: React Native/Expo frontend for uploading videos and viewing analysis results.

## 📚 Tech Stack 

- **Frontend**: React Native, Expo, JavaScript/TypeScript
- **Backend**: Python, FastAPI, Uvicorn
- **Computer Vision**: MediaPipe, OpenCV
- **Machine Learning / Signal Cleaning**: scikit-learn, NumPy, pandas
- **Database**: Supabase (PostgreSQL), SQLAlchemy
- **AI Integration**: OpenAI API

## 📸 Demo
<p align="center">
  <img src="screenshots/analyze" width="48%" alt="Throw Analysis">
  <img src="screenshots/top_compare" width="48%" alt="Throw History">
</p>

<p align="center">
  <img src="screenshots/history" width="48%" alt="Throw Comparison">
  <img src="screenshots/bottom_compare_1" width="48%" alt="Comparison Metrics">
</p>


## ⚙️ How It Works

### 📹 Video Processing and Pose Estimation

Using the MediaPipe pose detection Google framework, various different landmarks are tracked throughout the clip. With this comes a fair share of inaccurate and messy measurements, leading to signal cleaning using visibility and immediate jumps to filter through reliable landmark predictions, followed by interpolation and smoothing. From here, an assortment of metrics are created. 

### 🔎 Throw Detection and Biomechanical Analysis

Since most biomechanical metrics are calculated using the release frame, a Random Forest Classifier was trained to extract a throwing window, from the cocking of the arm to the release. From the predicted throw window, the pipeline then estimates the release frame, found by the frame with the maximum elbow angle

### 📝 Results and Feedback

Through FastAPI, the React-based frontend receives the metrics as a JSON response as well as the OpenAI generated coaching analysis. Supabase is integrated as well to store individual videos, with each row representing a new analysis, grouped by user. 

## 📊 Model Development Evaluation 

### Training Data and Feature Engineering

Before model training, each frame was assigned a binary label indicating whether it belonged to the throwing window. Features such as wrist height relative to the shoulder, elbow angle, and wrist-to-shoulder distance were extracted from the landmark data. Positional measurements were normalized using upper-arm or torso length to reduce the effects of differences in body size and camera distance. Rolling-window statistics were also introduced to capture changes in movement across consecutive frames rather than relying solely on individual-frame measurements.

### Model Evaluation and Cross Validation

A Random Forest classifier was trained using scikit-learn to identify throwing frames based on the engineered biomechanical features. To evaluate the model, 4-fold GroupKFold cross-validation was used, with frames grouped by their source video. Since neighboring frames within the same video are highly correlated, separating videos between training and testing prevents data leakage that could otherwise artificially inflate evaluation results. F1 score was prioritized as the primary evaluation metric to balance precision and recall, accounting for both false positives and false negatives. Since the throwing window typically consists of only 10 frames out of a 40–50 frame clip, accuracy alone could be misleading, as a model could achieve relatively high accuracy simply by predicting most frames as non-throwing.
  
