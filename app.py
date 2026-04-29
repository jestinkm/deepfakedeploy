from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import cv2
import numpy as np
import face_recognition
import subprocess
import base64
import os
import threading
import logging
import time

app = Flask(__name__)
CORS(app)

logging.basicConfig(level=logging.INFO)

# --- CONFIG ---
KNOWN_FACE = "static/justin.jpg"  # Path to known reference image
PRIVATE_FOLDER = r"E:\Justin"
MATCH_THRESHOLD = 0.60       # Open folder if accuracy >= 60%
RESIZE_SCALE = 0.25
AUTO_CLOSE_SECONDS = 10      # Close after 10 sec no match/no face
# ----------------

# Load known encoding
if not os.path.exists(KNOWN_FACE):
    raise FileNotFoundError(f"Known face image not found: {KNOWN_FACE}")

known_image = face_recognition.load_image_file(KNOWN_FACE)
known_encodings = face_recognition.face_encodings(known_image)
if not known_encodings:
    raise ValueError("No faces found in known face image.")
known_encoding = known_encodings[0]

# State variables
folder_open = False
last_match_time = 0
folder_open_lock = threading.Lock()


# ---------------- Permission Handling ----------------

def get_current_user():
    return os.getlogin()


def grant_access():
    user = get_current_user()
    cmd = f'icacls "{PRIVATE_FOLDER}" /grant:r "{user}:F"'
    os.system(cmd)
    logging.info(f"Access granted to {user}")


def revoke_access():
    user = get_current_user()
    cmd = f'icacls "{PRIVATE_FOLDER}" /deny "{user}:F"'
    os.system(cmd)
    logging.info(f"Access revoked for {user}")


# ---------------- Folder Open/Close ----------------

def open_folder():
    """Grant access and open folder in Explorer."""
    try:
        grant_access()
        logging.info("Opening folder: %s", PRIVATE_FOLDER)
        subprocess.Popen(["explorer", "/e,", PRIVATE_FOLDER], shell=True)
    except Exception as e:
        logging.exception("Failed to open folder: %s", e)


def close_folder_win32():
    """Close the folder window using Win32 API."""
    try:
        import win32gui
        import win32con
    except ImportError:
        logging.info("pywin32 not available - skipping win32 close.")
        return False

    basename = os.path.basename(PRIVATE_FOLDER)
    closed_any = False

    def enum_handler(hwnd, _):
        nonlocal closed_any
        if not win32gui.IsWindowVisible(hwnd):
            return
        title = win32gui.GetWindowText(hwnd) or ""
        if basename.lower() in title.lower():
            logging.info("Closing window HWND=%s Title=%s", hwnd, title)
            try:
                win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
                closed_any = True
            except Exception as e:
                logging.exception("Failed to send WM_CLOSE: %s", e)

    win32gui.EnumWindows(enum_handler, None)
    return closed_any


def close_folder_taskkill_fallback():
    """Fallback method using taskkill."""
    basename = os.path.basename(PRIVATE_FOLDER)
    cmd = f'taskkill /FI "WINDOWTITLE contains {basename}" /F'
    try:
        logging.info("Running fallback taskkill: %s", cmd)
        os.system(cmd)
        return True
    except Exception as e:
        logging.exception("taskkill fallback failed: %s", e)
        return False


def close_folder():
    """Close folder window and revoke access."""
    try:
        closed = close_folder_win32()
        if not closed:
            close_folder_taskkill_fallback()
        revoke_access()
        return True
    except Exception as e:
        logging.exception("Failed to close folder: %s", e)
        return False


# ---------------- Image Handling ----------------

def decode_base64_image(image_data_uri):
    """Convert base64 string to OpenCV image."""
    if not image_data_uri:
        return None
    if image_data_uri.startswith("data:"):
        parts = image_data_uri.split(",", 1)
        if len(parts) == 2:
            image_data_uri = parts[1]
    try:
        img_bytes = base64.b64decode(image_data_uri)
        np_arr = np.frombuffer(img_bytes, dtype=np.uint8)
        frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        return frame
    except Exception as e:
        logging.exception("Failed decoding base64 image: %s", e)
        return None


# ---------------- Flask Routes ----------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/check_face", methods=["POST"])
def check_face():
    global folder_open, last_match_time
    data = request.get_json(force=True, silent=True) or {}
    image_data = data.get("image")

    frame = decode_base64_image(image_data)
    if frame is None:
        return jsonify({"status": "error", "message": "Image decoding failed"}), 400

    small_frame = cv2.resize(frame, (0, 0), fx=RESIZE_SCALE, fy=RESIZE_SCALE)
    rgb_small = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_small, model="hog")
    matched = False
    best_accuracy = 0.0

    if face_locations:
        face_encodings = face_recognition.face_encodings(rgb_small, face_locations)
        for enc in face_encodings:
            distance = face_recognition.face_distance([known_encoding], enc)[0]
            confidence = max(0.0, min(1.0, 1.0 - distance))
            accuracy_pct = confidence * 100.0
            if accuracy_pct > best_accuracy:
                best_accuracy = accuracy_pct
            if confidence >= MATCH_THRESHOLD:
                matched = True
                break
    else:
        best_accuracy = 0.0

    with folder_open_lock:
        if matched:
            last_match_time = time.time()
            if not folder_open:
                open_folder()
                folder_open = True
            return jsonify({
                "status": "opened" if not folder_open else "unchanged",
                "matched": True,
                "accuracy": round(best_accuracy, 2)
            })
        else:
            if folder_open and (time.time() - last_match_time > AUTO_CLOSE_SECONDS):
                close_folder()
                folder_open = False
                return jsonify({
                    "status": "closed",
                    "matched": False,
                    "accuracy": round(best_accuracy, 2)
                })

    return jsonify({
        "status": "unchanged",
        "matched": matched,
        "accuracy": round(best_accuracy, 2)
    })


if __name__ == "__main__":
    # Production deployment settings
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host="0.0.0.0", port=port)
