import os
import platform
import winsound

def play_buzzer():
    system = platform.system()
    if system == "Windows":
        # Use built-in beep
        winsound.Beep(1000, 500)  # Frequency: 1000Hz, Duration: 500ms
    else:
        # For Linux/macOS
        os.system('echo -e "\a"')

def send_notification(frame):
    print("🚨 Crime Detected! Saving alert frame...")
    play_buzzer()
    saved_path = save_alert_frame(frame)
    print(f"📸 Frame saved at: {saved_path}")
    return saved_path
