# app.py
# pylint: disable=no-member

import streamlit as st
import cv2
import tempfile
import os
import time

from detector import predict_frame
from utils.notify import send_notification

# ---------------- Page Config ----------------
st.set_page_config(page_title="Live CCTV Crime Detection", layout="wide")

st.title("🔴 Live CCTV Crime Detection System")
st.markdown(
    "Upload a CCTV video to detect any violence or crime. "
    "Alerts will be shown and detected frames will be saved."
)

# ---------------- Session State ----------------
if "processing" not in st.session_state:
    st.session_state.processing = False

# ---------------- Upload ----------------
uploaded_video = st.file_uploader(
    "📤 Upload a Video File",
    type=["mp4", "avi", "mov"]
)

# ---------------- Start Button ----------------
if uploaded_video and st.button("▶ Start Processing"):
    st.session_state.processing = True

# ---------------- Processing ----------------
if uploaded_video and st.session_state.processing:

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tfile:
        tfile.write(uploaded_video.read())
        video_path = tfile.name

    st.info("⏳ Processing video... Please wait.")

    cap = cv2.VideoCapture(video_path)

    frame_display = st.empty()
    alert_placeholder = st.empty()

    alert_triggered = False
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # ✅ Increment frame count FIRST
        frame_count += 1

        # ✅ Skip frames (every 5th frame only)
        if frame_count % 5 != 0:
            continue

        # Convert BGR → RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Display frame
        frame_display.image(
            frame_rgb,
            channels="RGB",
            caption=f"Frame {frame_count}"
        )

        # Detection
        is_crime = predict_frame(frame)

        # Debug output
        st.write(f"Frame {frame_count} → Prediction: {is_crime}")

        # Alert logic
        if is_crime and not alert_triggered:
            saved_path = send_notification(frame)
            alert_placeholder.error(
                f"🚨 Crime Detected! Frame saved at `{saved_path}`"
            )
            alert_triggered = True

        if not is_crime:
            alert_triggered = False

        # Prevent UI freeze
        time.sleep(0.03)

    cap.release()

    if os.path.exists(video_path):
        os.remove(video_path)

    st.session_state.processing = False
    st.success("✅ Video processing complete.")
