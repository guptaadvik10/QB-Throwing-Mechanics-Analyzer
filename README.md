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
<img src="screenshots/analyze" alt="Throw Analysis" width="750">


  
