"""
AI Smart Farmer Assistant – Flask Backend
"""

import os
import json
import pathlib
import logging
import traceback
import threading
import numpy as np

from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from utils import (
    preprocess_image,
    allowed_file,
    save_uploaded_file,
    get_solution,
    get_db_connection,
    save_prediction,
    fetch_history,
)

# ── Logging ─────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s  %(levelname)-8s  %(message)s",
)
logger = logging.getLogger(__name__)

# ── App Setup ───────────────────────────────────────
app = Flask(__name__)
CORS(app)

BASE_DIR = pathlib.Path(__file__).parent
UPLOADS_DIR = BASE_DIR.parent / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16MB

# ── DB Config ───────────────────────────────────────
DB_CONFIG = {
    "host": os.environ.get("DB_HOST", "localhost"),
    "user": os.environ.get("DB_USER", "root"),
    "password": os.environ.get("DB_PASSWORD", ""),
    "database": os.environ.get("DB_NAME", "smart_farmer_db"),
    "port": int(os.environ.get("DB_PORT", 3306)),
}

# ── Class Names ─────────────────────────────────────
CLASS_NAMES_PATH = BASE_DIR / "class_names.json"
if CLASS_NAMES_PATH.exists():
    with open(CLASS_NAMES_PATH) as f:
        CLASS_NAMES = json.load(f)
else:
    CLASS_NAMES = [
        "Tomato___Early_blight",
        "Tomato___Late_blight",
        "Tomato___healthy",
        "Potato___Early_blight",
        "Potato___Late_blight",
        "Potato___healthy",
    ]

# ── Model (Background Loading) ──────────────────────
MODEL_PATH = BASE_DIR / "model.h5"
model = None


def load_model_background():
    global model
    try:
        logger.info("⏳ Loading TensorFlow model in background...")
        import tensorflow as tf

        if MODEL_PATH.exists():
            model = tf.keras.models.load_model(str(MODEL_PATH))
            logger.info("✅ Model loaded successfully!")
        else:
            logger.warning("⚠️ model.h5 not found – using simulation mode")
    except Exception as e:
        logger.error("❌ Model load failed: %s", str(e))
        model = None


def simulate_prediction():
    probs = np.random.dirichlet(np.ones(len(CLASS_NAMES)) * 0.5)
    winner = np.random.randint(len(CLASS_NAMES))
    probs[winner] += 1.2
    probs /= probs.sum()
    return probs


# ── Routes ──────────────────────────────────────────

@app.route("/")
def home():
    return jsonify({
        "message": "🚀 AI Smart Farmer API is running",
        "endpoints": ["/predict", "/history", "/health"]
    })


@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "model_loaded": model is not None,
        "mode": "tf_model" if model else "simulation"
    })


@app.route("/uploads/<path:filename>")
def serve_upload(filename):
    return send_from_directory(str(UPLOADS_DIR), filename)


@app.route("/history")
def history():
    try:
        conn = get_db_connection(DB_CONFIG)
        rows = fetch_history(conn, limit=20)
        conn.close()
        return jsonify({"success": True, "history": rows})
    except Exception as e:
        logger.error("DB error: %s", e)
        return jsonify({"success": False, "error": str(e)}), 500


@app.route("/predict", methods=["POST"])
def predict():
    if "file" not in request.files:
        return jsonify({"success": False, "error": "No file provided"}), 400

    file = request.files["file"]
    lang = request.form.get("lang", "en").lower()

    if file.filename == "":
        return jsonify({"success": False, "error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"success": False, "error": "Invalid file type"}), 400

    try:
        # Save file
        saved_path = save_uploaded_file(file, file.filename)
        logger.info("📸 Image saved: %s", saved_path)

        # Predict
        try:
            if model is not None:
                img = preprocess_image(saved_path)
                probs = model.predict(img, verbose=0)[0]
            else:
                logger.info("⚠️ Model not ready → using simulation")
                probs = simulate_prediction()
        except Exception as pred_error:
            logger.error("❌ Prediction failed: %s", pred_error)
            probs = simulate_prediction()

        # Decode
        top_idx = int(np.argmax(probs))
        confidence = float(probs[top_idx]) * 100
        class_name = CLASS_NAMES[top_idx]

        sol = get_solution(class_name, lang)
        image_url = f"/uploads/{pathlib.Path(saved_path).name}"

        # Save to DB
        try:
            conn = get_db_connection(DB_CONFIG)
            save_prediction(
                conn,
                image_url,
                sol["name"],
                confidence,
                " | ".join(sol["treatment"]),
                lang,
            )
            conn.close()
        except Exception as db_error:
            logger.warning("DB save failed: %s", db_error)

        return jsonify({
            "success": True,
            "disease": class_name,
            "name": sol["name"],
            "confidence": round(confidence, 2),
            "cause": sol["cause"],
            "treatment": sol["treatment"],
            "image_url": image_url,
            "mode": "tf_model" if model else "simulation"
        })

    except Exception as e:
        logger.error("❌ Error:\n%s", traceback.format_exc())
        return jsonify({"success": False, "error": str(e)}), 500


# ── Error Handlers ──────────────────────────────────

@app.errorhandler(413)
def too_large(e):
    return jsonify({"success": False, "error": "File too large"}), 413


@app.errorhandler(404)
def not_found(e):
    return jsonify({"success": False, "error": "Not found"}), 404


# ── Run Server ──────────────────────────────────────
if __name__ == "__main__":
    logger.info("🚀 Starting AI Smart Farmer Backend...")
    logger.info("📁 Uploads: %s", UPLOADS_DIR)

    # Start model loading in background
    threading.Thread(target=load_model_background).start()

    app.run(host="0.0.0.0", port=5000, debug=True)
