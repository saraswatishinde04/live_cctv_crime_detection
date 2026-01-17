# utils/notify.py

import os
import cv2
import time

ALERT_DIR = "saved_alerts"


def save_alert_frame(frame):
    """Save detected crime frame to disk and return path"""
    os.makedirs(ALERT_DIR, exist_ok=True)

    timestamp = time.strftime("%Y%m%d_%H%M%S")
    filename = f"alert_{timestamp}.jpg"
    path = os.path.join(ALERT_DIR, filename)

    cv2.imwrite(path, frame)
    return path


def send_notification(frame):
    """
    Handles alert logic (currently saves frame).
    Can be extended to email / buzzer / WhatsApp.
    """
    saved_path = save_alert_frame(frame)
    return saved_path
