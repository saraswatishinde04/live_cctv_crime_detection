# app.py
# pylint: disable=no-member

import streamlit as st
import cv2
import tempfile
import os
import time

from detector import predict_frame
from utils.notify import send_notification

st.set_page_config(page_title="Live CCTV Crime Detection", layout="wide")

st.title("🔴 Live CCTV Crime Detection System")
st.markdown(
    "Upload a CCTV video to detect any violence or crime. "
    "Alerts will be shown and detected frames will be saved."
)

# Initialize session state
if "processing" not in st.session_state:
    st.session_state.processing = False

uploaded_video = st.file_uploader(
    "📤 Upload a Video File",
    type=["mp4", "avi", "mov"]
)

# Start button (CRITICAL)
if uploaded_video and st.button("▶ Start Processing"):
    st.session_state.processing = True

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

        frame_count += 1

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame_display.image(
            frame_rgb,
            channels="RGB",
            caption=f"Frame {frame_count}"
        )

        is_crime = predict_frame(frame)

        if is_crime and not alert_triggered:
            saved_path = send_notification(frame)
            alert_placeholder.error(
                f"🚨 Crime Detected! Frame saved at `{saved_path}`"
            )
            alert_triggered = True

        if not is_crime:
            alert_triggered = False

        time.sleep(0.03)  # prevent UI freeze

    cap.release()
    os.remove(video_path)

    st.session_state.processing = False
    st.success("✅ Video processing complete.")
