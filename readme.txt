# Hand Tracking Control  

This project uses OpenCV, MediaPipe, and PyCAW to implement real-time hand gesture control. It tracks both hands through a webcam:  

- **Left Hand → Controls Screen Brightness**  
- **Right Hand → Controls System Volume**  

---

## 📂 Project Structure  
HandTrackingProject/
│── HandTrackingModule.py   # Custom module for hand tracking (built on MediaPipe)
│── main.py     # Main script to run the hand gesture control system
│── requirements.txt    # Project dependencies
│── README.md   # Project documentation


---

## ⚙️ Features  

- Real-time hand detection and tracking using **MediaPipe Hands**  
- Brightness Control with left-hand gestures  
- Volume Control with right-hand gestures  
- Smooth gesture-to-action mapping with OpenCV visualization  

---

## 🚀 Installation  

1. Clone the repository or download the files  
2. Install dependencies:  

   ```bash
   
   pip install -r requirements.txt

##📦 Dependencies

opencv-python

mediapipe

numpy

screen-brightness-control

comtypes

pycaw
