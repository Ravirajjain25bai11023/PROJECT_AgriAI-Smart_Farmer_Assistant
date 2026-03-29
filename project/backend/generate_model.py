"""
generate_model.py
=================
Run this ONCE to create a dummy model.h5 for the Smart Farmer app.
In production, replace with a model trained on the PlantVillage dataset.

Usage:
    python generate_model.py
"""

import numpy as np

# ── Try importing TensorFlow ──────────────────────────────────────────────────
try:
    import tensorflow as tf
    from tensorflow.keras import layers, models
    TF_AVAILABLE = True
except ImportError:
    TF_AVAILABLE = False
    print("TensorFlow not found. Generating a mock model file instead.")

# ── Class labels (PlantVillage-inspired) ──────────────────────────────────────
CLASS_NAMES = [
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Corn___Cercospora_leaf_spot",
    "Corn___Common_rust",
    "Corn___Northern_Leaf_Blight",
    "Corn___healthy",
]

NUM_CLASSES = len(CLASS_NAMES)
IMG_SIZE    = 224


def build_cnn_model():
    """Build a lightweight CNN (MobileNet-style architecture)."""
    model = models.Sequential([
        # ── Block 1 ──────────────────────────────────────────────────────────
        layers.Conv2D(32, (3, 3), activation="relu", padding="same",
                      input_shape=(IMG_SIZE, IMG_SIZE, 3)),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),

        # ── Block 2 ──────────────────────────────────────────────────────────
        layers.Conv2D(64, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),

        # ── Block 3 ──────────────────────────────────────────────────────────
        layers.Conv2D(128, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.MaxPooling2D(2, 2),

        # ── Block 4 ──────────────────────────────────────────────────────────
        layers.Conv2D(256, (3, 3), activation="relu", padding="same"),
        layers.BatchNormalization(),
        layers.GlobalAveragePooling2D(),

        # ── Classifier head ──────────────────────────────────────────────────
        layers.Dense(512, activation="relu"),
        layers.Dropout(0.4),
        layers.Dense(NUM_CLASSES, activation="softmax"),
    ], name="SmartFarmerCNN")

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"],
    )
    return model


if TF_AVAILABLE:
    print("Building CNN model …")
    model = build_cnn_model()
    model.summary()
    model.save("model.h5")
    print(f"\n✅  model.h5 saved  ({NUM_CLASSES} classes)")
else:
    # ── Fallback: write a minimal marker file so Flask can detect absence ──
    import json, pathlib
    meta = {"classes": CLASS_NAMES, "img_size": IMG_SIZE, "note": "dummy"}
    pathlib.Path("model_meta.json").write_text(json.dumps(meta, indent=2))
    print("✅  model_meta.json written (TF not available; simulation mode).")

# ── Save class list for use by Flask ─────────────────────────────────────────
import json, pathlib
pathlib.Path("class_names.json").write_text(
    json.dumps(CLASS_NAMES, indent=2, ensure_ascii=False)
)
print("✅  class_names.json saved.")
