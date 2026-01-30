import warnings
warnings.filterwarnings('ignore', category=UserWarning)
warnings.filterwarnings('ignore', category=DeprecationWarning)

import os
import sys
import json
import numpy as np
import joblib
import tensorflow as tf
from fastapi import FastAPI, File, UploadFile
from PIL import Image
import io
from fastapi.responses import JSONResponse

# 1. Force TensorFlow 2.x behavior
os.environ['TF_USE_LEGACY_KERAS'] = '0'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# 2. Force clean TensorFlow import
if 'tensorflow' in sys.modules:
    del sys.modules['tensorflow']
if 'keras' in sys.modules:
    del sys.modules['keras']

app = FastAPI()

# ========== PATHS ==========
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Model paths
CROP_MODEL_PATH = os.path.join(BASE_DIR, "models", "xgb_crop_model.pkl")
CROP_SCALER_PATH = os.path.join(BASE_DIR, "models", "minmax_scaler.pkl")
DISEASE_MODEL_PATH = os.path.join(BASE_DIR, "models", "Crop_Disease_Model (1).keras")

# Translation paths
CROP_TRANSLATIONS_PATH = os.path.join(BASE_DIR, "translations", "crop_pred_translations.json")
DISEASE_TRANSLATIONS_PATH = os.path.join(BASE_DIR, "translations", "crop_disease_translations.json")

# ========== LOAD TRANSLATIONS ==========
with open(CROP_TRANSLATIONS_PATH, "r", encoding="utf-8") as f:
    crop_translations = json.load(f)
with open(DISEASE_TRANSLATIONS_PATH, "r", encoding="utf-8") as f:
    disease_translations = json.load(f)

# ========== SUPPORTED LANGUAGES ==========
SUPPORTED_LANGUAGES = {
    "english": "en", "eng": "en", "en": "en",
    "hindi": "hi", "hin": "hi", "hi": "hi",
    "bengali": "bn", "ben": "bn", "bn": "bn", "bangla": "bn",
    "telugu": "te", "tel": "te", "te": "te",
    "marathi": "mr", "mar": "mr", "mr": "mr",
    "tamil": "ta", "tam": "ta", "ta": "ta",
    "kannada": "kn", "kan": "kn", "kn": "kn",
    "punjabi": "pa", "pun": "pa", "pa": "pa", "panjabi": "pa"
}

# ========== LOAD MODELS ==========
# Load crop model
crop_model = joblib.load(CROP_MODEL_PATH)
crop_scaler = joblib.load(CROP_SCALER_PATH)
print("✓ Crop model and scaler loaded")

# Load disease model
tf.keras.backend.clear_session()
try:
    disease_model = tf.keras.models.load_model(
        DISEASE_MODEL_PATH,
        custom_objects={'KerasLayer': tf.keras.layers.Layer}
    )
    print("✓ Disease model loaded")
except Exception as e:
    print(f"✗ Error loading disease model: {e}")
    disease_model = None

# ========== CROP LABELS ==========
crop_labels = [
    'apple', 'banana', 'blackgram', 'chickpea', 'coconut', 'coffee',
    'cotton', 'grapes', 'jute', 'kidneybeans', 'lentil', 'maize',
    'mango', 'mothbeans', 'mungbean', 'muskmelon', 'orange',
    'papaya', 'pigeonpeas', 'pomegranate', 'rice', 'watermelon'
]

# ========== API ENDPOINTS ==========
@app.get("/")
async def root():
    return {
        "message": "Crop & Disease Prediction API",
        "endpoints": {
            "crop": "/predict-crop - POST with N, P, K, temperature, humidity, ph, rainfall",
            "disease": "/predict-disease - POST with image file (file upload or base64)"
        },
        "languages": list(SUPPORTED_LANGUAGES.keys())
    }

@app.post("/predict-crop")
async def predict_crop(
    N: int, P: int, K: int,
    temperature: float, humidity: float,
    ph: float, rainfall: float,
    language: str = "english"
):
    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        language = "english"
    lang_code = SUPPORTED_LANGUAGES[language]
    
    # Prepare input
    raw_input = np.array([[N, P, K, temperature, humidity, ph, rainfall]], dtype=np.float32)
    scaled_input = crop_scaler.transform(raw_input)
    probabilities = crop_model.predict_proba(scaled_input)[0]
    
    # Get predictions
    top1_index = np.argmax(probabilities)
    top3_indices = np.argsort(probabilities)[-3:][::-1]
    
    # Translate results
    predicted_crop_translated = crop_translations[str(top1_index)][lang_code]
    
    top_3 = [
        {
            "class": crop_translations[str(i)][lang_code],
            "confidence": float(probabilities[i])
        }
        for i in top3_indices
    ]
    
    return {
        "predicted_crop": predicted_crop_translated,
        "confidence": round(float(probabilities[top1_index]), 4),
        "top_3_predictions": top_3,
        "language": language
    }

@app.post("/predict-disease")
async def predict_disease(
    file: UploadFile = File(None),
    base64_image: str = None,
    language: str = "english"
):
    # Check if model loaded
    if disease_model is None:
        return {"error": "Disease model not available"}
    
    # Validate language
    if language not in SUPPORTED_LANGUAGES:
        language = "english"
    lang_code = SUPPORTED_LANGUAGES[language]
    
    try:
        # Get image from file or base64
        if file and file.filename:
            image_bytes = await file.read()
        elif base64_image:
            import base64
            image_bytes = base64.b64decode(base64_image)
        else:
            return {"error": "No image provided"}
        
        # Process image
        image = Image.open(io.BytesIO(image_bytes))
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        image = image.resize((224, 224))
        img_array = np.array(image).astype('float32')
        img_array = tf.keras.applications.efficientnet.preprocess_input(img_array)
        img_array = np.expand_dims(img_array, axis=0)
        
        # Predict
        predictions = disease_model.predict(img_array, verbose=0)
        predicted_idx = np.argmax(predictions[0])
        top_3_indices = np.argsort(predictions[0])[-3:][::-1]
        
        # Translate results
        predicted_disease_translated = disease_translations[str(predicted_idx)][lang_code]
        
        top_3 = [
            {
                "class": disease_translations[str(i)][lang_code],
                "confidence": float(predictions[0][i])
            }
            for i in top_3_indices
        ]
        
        return {
            "predicted_disease": predicted_disease_translated,
            "confidence": round(float(predictions[0][predicted_idx]), 4),
            "top_3_predictions": top_3,
            "language": language
        }
        
    except Exception as e:
        return {"error": f"Prediction failed: {str(e)}"}