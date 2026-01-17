# app.py
# pylint: disable=no-member

import streamlit as st
import cv2
import tempfile
import os
import time

from detector import predict_frame
from utils.notify import send_notification

# ------------------ Streamlit Page Config ------------------
st.set_page_config(
    page_title="Live CCTV Crime Detection",
    layout="wide"
)

st.title("🔴 Live CCTV Crime Detection System")
st.markdown(
    "Upload a CCTV video to detect any violence or crime. "
    "Alerts will be shown and detected frames will be saved."
)

# ------------------ Video Upload ------------------
uploaded_video = st.file_uploader(
    "📤 Upload a Video File",
    type=["mp4", "avi", "mov"]
)

if uploaded_video is not None:

    # Save uploaded video temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tfile:
        tfile.write(uploaded_video.read())
        video_path = tfile.name

    st.info("⏳ Processing video... Please wait.")

    # OpenCV Video Capture
    cap = cv2.VideoCapture(video_path)

    frame_display = st.empty()
    alert_placeholder = st.empty()

    alert_triggered = False
    frame_count = 0

    # ------------------ Frame Processing Loop ------------------
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        frame_count += 1

        # Convert BGR to RGB
