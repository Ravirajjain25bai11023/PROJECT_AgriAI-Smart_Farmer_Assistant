import os
import json
import pathlib
import datetime
import logging

import numpy as np
from PIL import Image

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

IMG_SIZE    = 224
UPLOADS_DIR = pathlib.Path(__file__).parent.parent / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

SOLUTIONS = {
    #Tomato 
    "Tomato___Bacterial_spot": {
        "en": {
            "name": "Tomato – Bacterial Spot",
            "cause": "Caused by Xanthomonas bacteria spread by rain splash and infected seeds.",
            "treatment": [
                "Remove and destroy infected plant parts immediately.",
                "Apply copper-based bactericide (e.g., Bordeaux mixture) every 7–10 days.",
                "Avoid overhead irrigation; use drip irrigation instead.",
                "Use certified disease-free seeds for next season.",
                "Rotate crops — avoid tomato family for 2 years.",
            ],
        },
        "hi": {
            "name": "टमाटर – बैक्टीरियल स्पॉट",
            "cause": "यह Xanthomonas बैक्टीरिया से होता है जो बारिश की बूंदों और संक्रमित बीजों से फैलता है।",
            "treatment": [
                "संक्रमित पत्तियों को तुरंत हटाएं और नष्ट करें।",
                "कॉपर आधारित कीटनाशक (बोर्डो मिश्रण) हर 7–10 दिन में छिड़कें।",
                "सिंचाई के लिए ड्रिप विधि अपनाएं, ऊपर से पानी न दें।",
                "अगले सीजन में प्रमाणित बीजों का उपयोग करें।",
                "फसल चक्र अपनाएं — 2 साल तक टमाटर परिवार से बचें।",
            ],
        },
    },
    "Tomato___Early_blight": {
        "en": {
            "name": "Tomato – Early Blight",
            "cause": "Caused by Alternaria solani fungus; thrives in warm, humid conditions.",
            "treatment": [
                "Apply fungicide containing chlorothalonil or mancozeb every 7–14 days.",
                "Remove lower infected leaves to improve air circulation.",
                "Mulch around plants to prevent soil splash.",
                "Water at the base of plants early in the morning.",
                "Plant resistant varieties in the next crop cycle.",
            ],
        },
        "hi": {
            "name": "टमाटर – अर्ली ब्लाइट",
            "cause": "Alternaria solani फंगस के कारण; गर्म और आर्द्र मौसम में पनपता है।",
            "treatment": [
                "क्लोरोथैलोनिल या मैंकोजेब युक्त कवकनाशी हर 7–14 दिन में छिड़कें।",
                "नीचे की संक्रमित पत्तियां हटाएं।",
                "पौधों के चारों ओर मल्च बिछाएं।",
                "सुबह पौधे की जड़ में पानी दें।",
                "अगली फसल में प्रतिरोधी किस्म लगाएं।",
            ],
        },
    },
    "Tomato___Late_blight": {
        "en": {
            "name": "Tomato – Late Blight",
            "cause": "Caused by Phytophthora infestans; devastating in cool, wet weather.",
            "treatment": [
                "Apply metalaxyl + mancozeb fungicide immediately.",
                "Destroy all infected plants — do NOT compost them.",
                "Improve field drainage to reduce humidity.",
                "Apply preventive copper sprays before rain forecast.",
                "Avoid planting tomatoes near potatoes.",
            ],
        },
        "hi": {
            "name": "टमाटर – लेट ब्लाइट",
            "cause": "Phytophthora infestans से; ठंडे, नम मौसम में तेजी से फैलता है।",
            "treatment": [
                "मेटालैक्सिल + मैंकोजेब कवकनाशी तुरंत लगाएं।",
                "संक्रमित पौधों को नष्ट करें — खाद में न डालें।",
                "खेत में जल निकासी सुधारें।",
                "बारिश से पहले कॉपर स्प्रे करें।",
                "टमाटर को आलू के पास न लगाएं।",
            ],
        },
    },
    "Tomato___Leaf_Mold": {
        "en": {
            "name": "Tomato – Leaf Mold",
            "cause": "Caused by Passalora fulva fungus; common in greenhouses with high humidity.",
            "treatment": [
                "Increase ventilation in greenhouse or open field spacing.",
                "Apply fungicide (chlorothalonil or copper-based).",
                "Avoid wetting leaves during irrigation.",
                "Remove and destroy affected leaves promptly.",
                "Maintain relative humidity below 85%.",
            ],
        },
        "hi": {
            "name": "टमाटर – लीफ मोल्ड",
            "cause": "Passalora fulva फंगस; ग्रीनहाउस में अधिक नमी से होता है।",
            "treatment": [
                "ग्रीनहाउस में हवा का प्रवाह बढ़ाएं।",
                "कवकनाशी (क्लोरोथैलोनिल या कॉपर) छिड़कें।",
                "सिंचाई में पत्तियां न भिगोएं।",
                "प्रभावित पत्तियां जल्दी हटाएं।",
                "सापेक्ष आर्द्रता 85% से नीचे रखें।",
            ],
        },
    },
    "Tomato___Septoria_leaf_spot": {
        "en": {
            "name": "Tomato – Septoria Leaf Spot",
            "cause": "Caused by Septoria lycopersici fungus; spreads through rain and tools.",
            "treatment": [
                "Apply mancozeb or chlorothalonil fungicide every 10 days.",
                "Remove and dispose of infected lower leaves.",
                "Stake plants to improve airflow.",
                "Sanitize tools with 10% bleach solution.",
                "Rotate crops every 2–3 years.",
            ],
        },
        "hi": {
            "name": "टमाटर – सेप्टोरिया लीफ स्पॉट",
            "cause": "Septoria lycopersici फंगस; बारिश और औजारों से फैलता है।",
            "treatment": [
                "हर 10 दिन में मैंकोजेब या क्लोरोथैलोनिल छिड़कें।",
                "निचली संक्रमित पत्तियां हटाएं।",
                "पौधों को सहारा दें।",
                "औजारों को 10% ब्लीच से साफ करें।",
                "2–3 साल में फसल बदलें।",
            ],
        },
    },
    "Tomato___Spider_mites": {
        "en": {
            "name": "Tomato – Spider Mites (Two-spotted)",
            "cause": "Tiny arachnids thrive in hot, dry conditions; suck plant sap.",
            "treatment": [
                "Spray neem oil solution (2%) every 5–7 days.",
                "Apply miticide (abamectin or bifenazate).",
                "Increase humidity around plants using irrigation.",
                "Introduce predatory mites (Phytoseiulus persimilis) as biocontrol.",
                "Remove heavily infested leaves.",
            ],
        },
        "hi": {
            "name": "टमाटर – स्पाइडर माइट्स",
            "cause": "सूक्ष्म कीट गर्म, सूखे मौसम में पनपते हैं।",
            "treatment": [
                "नीम तेल (2%) हर 5–7 दिन में छिड़कें।",
                "माइटिसाइड (एबामेक्टिन) लगाएं।",
                "सिंचाई से आर्द्रता बढ़ाएं।",
                "जैव नियंत्रण के लिए परभक्षी माइट्स छोड़ें।",
                "बुरी तरह प्रभावित पत्तियां हटाएं।",
            ],
        },
    },
    "Tomato___Target_Spot": {
        "en": {
            "name": "Tomato – Target Spot",
            "cause": "Caused by Corynespora cassiicola fungus in warm, humid environments.",
            "treatment": [
                "Apply azoxystrobin or difenoconazole fungicide.",
                "Ensure adequate plant spacing for airflow.",
                "Avoid overhead irrigation.",
                "Remove infected debris after harvest.",
                "Use resistant cultivars.",
            ],
        },
        "hi": {
            "name": "टमाटर – टारगेट स्पॉट",
            "cause": "Corynespora cassiicola फंगस; गर्म, आर्द्र वातावरण में।",
            "treatment": [
                "एज़ॉक्सिस्ट्रोबिन या डाइफेनोकोनाज़ोल कवकनाशी लगाएं।",
                "पौधों के बीच पर्याप्त दूरी रखें।",
                "ऊपर से पानी न दें।",
                "कटाई के बाद संक्रमित अवशेष हटाएं।",
                "प्रतिरोधी किस्म का चयन करें।",
            ],
        },
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "en": {
            "name": "Tomato – Yellow Leaf Curl Virus (TYLCV)",
            "cause": "Transmitted by whiteflies (Bemisia tabaci); no cure once infected.",
            "treatment": [
                "Control whitefly populations with imidacloprid or thiamethoxam.",
                "Use yellow sticky traps to monitor and reduce whiteflies.",
                "Remove and destroy all infected plants immediately.",
                "Plant reflective mulch to deter whiteflies.",
                "Use TYLCV-resistant tomato varieties in future plantings.",
            ],
        },
        "hi": {
            "name": "टमाटर – येलो लीफ कर्ल वायरस",
            "cause": "सफेद मक्खी (Bemisia tabaci) से फैलता है; संक्रमण का इलाज नहीं।",
            "treatment": [
                "इमिडाक्लोप्रिड से सफेद मक्खी नियंत्रित करें।",
                "पीले स्टिकी ट्रैप लगाएं।",
                "संक्रमित पौधों को तुरंत हटाएं।",
                "परावर्तक मल्च का उपयोग करें।",
                "अगली फसल में TYLCV-प्रतिरोधी किस्म लगाएं।",
            ],
        },
    },
    "Tomato___Tomato_mosaic_virus": {
        "en": {
            "name": "Tomato – Mosaic Virus (ToMV)",
            "cause": "Mechanically transmitted via contaminated hands, tools, and insects.",
            "treatment": [
                "Wash hands thoroughly before handling plants.",
                "Sterilize all tools with 10% bleach or 70% alcohol.",
                "Remove and destroy infected plants.",
                "Control aphids and other insect vectors.",
                "Plant certified virus-free seeds or transplants.",
            ],
        },
        "hi": {
            "name": "टमाटर – मोज़ेक वायरस",
            "cause": "हाथों, औजारों और कीड़ों से फैलता है।",
            "treatment": [
                "पौधों को छूने से पहले हाथ धोएं।",
                "सभी औजार ब्लीच से स्टरलाइज़ करें।",
                "संक्रमित पौधे नष्ट करें।",
                "एफिड और अन्य कीड़ों को नियंत्रित करें।",
                "प्रमाणित वायरस-मुक्त बीज लगाएं।",
            ],
        },
    },
    "Tomato___healthy": {
        "en": {
            "name": "Tomato – Healthy",
            "cause": "No disease detected. Plant appears healthy.",
            "treatment": [
                "Continue regular watering and fertilization schedule.",
                "Monitor weekly for early signs of pests or disease.",
                "Maintain proper plant spacing for good airflow.",
                "Apply preventive neem oil spray monthly.",
                "Great job — keep up the good farming practices!",
            ],
        },
        "hi": {
            "name": "टमाटर – स्वस्थ",
            "cause": "कोई बीमारी नहीं मिली। पौधा स्वस्थ दिखता है।",
            "treatment": [
                "नियमित सिंचाई और खाद जारी रखें।",
                "सप्ताह में एक बार कीड़ों की जांच करें।",
                "पौधों के बीच उचित दूरी रखें।",
                "महीने में एक बार नीम तेल का निवारक छिड़काव करें।",
                "बढ़िया! अच्छी खेती की आदतें बनाए रखें।",
            ],
        },
    },
    #Potato
    "Potato___Early_blight": {
        "en": {
            "name": "Potato – Early Blight",
            "cause": "Caused by Alternaria solani; occurs in warm, wet weather on older leaves.",
            "treatment": [
                "Apply mancozeb or chlorothalonil fungicide every 7–10 days.",
                "Remove and destroy infected leaves.",
                "Avoid excessive nitrogen fertilization.",
                "Ensure good drainage in the field.",
                "Use certified disease-free seed potatoes.",
            ],
        },
        "hi": {
            "name": "आलू – अर्ली ब्लाइट",
            "cause": "Alternaria solani; गर्म, गीले मौसम में पुरानी पत्तियों पर।",
            "treatment": [
                "हर 7–10 दिन में मैंकोजेब कवकनाशी छिड़कें।",
                "संक्रमित पत्तियां हटाएं।",
                "अत्यधिक नाइट्रोजन खाद से बचें।",
                "खेत में जल निकासी सुनिश्चित करें।",
                "प्रमाणित बीज आलू का उपयोग करें।",
            ],
        },
    },
    "Potato___Late_blight": {
        "en": {
            "name": "Potato – Late Blight",
            "cause": "Caused by Phytophthora infestans; the pathogen behind the Irish Famine.",
            "treatment": [
                "Apply metalaxyl + mancozeb fungicide immediately.",
                "Destroy all infected tubers and plant material.",
                "Hill up soil around potato rows to protect tubers.",
                "Improve field drainage significantly.",
                "Plant resistant varieties like Sarpo Mira or Cara.",
            ],
        },
        "hi": {
            "name": "आलू – लेट ब्लाइट",
            "cause": "Phytophthora infestans; ठंडे, नम मौसम में विनाशकारी।",
            "treatment": [
                "मेटालैक्सिल + मैंकोजेब तुरंत लगाएं।",
                "सभी संक्रमित कंद और पौधे नष्ट करें।",
                "आलू की कतारों के चारों ओर मिट्टी चढ़ाएं।",
                "जल निकासी सुधारें।",
                "प्रतिरोधी किस्में लगाएं।",
            ],
        },
    },
    "Potato___healthy": {
        "en": {
            "name": "Potato – Healthy",
            "cause": "No disease detected. Crop appears healthy.",
            "treatment": [
                "Maintain regular watering; avoid waterlogging.",
                "Apply balanced NPK fertilizer as per soil test.",
                "Scout weekly for Colorado potato beetle.",
                "Hill up soil when plants reach 15–20 cm.",
                "Excellent — your crop management is working well!",
            ],
        },
        "hi": {
            "name": "आलू – स्वस्थ",
            "cause": "कोई बीमारी नहीं। फसल स्वस्थ है।",
            "treatment": [
                "नियमित सिंचाई करें; जलभराव से बचें।",
                "मिट्टी परीक्षण के अनुसार NPK खाद दें।",
                "कोलोराडो बीटल की साप्ताहिक जांच करें।",
                "15–20 सेमी पर पौधों के चारों ओर मिट्टी चढ़ाएं।",
                "शानदार — आपकी फसल प्रबंधन सही है!",
            ],
        },
    },
    #Corn
    "Corn___Cercospora_leaf_spot": {
        "en": {
            "name": "Corn – Gray Leaf Spot (Cercospora)",
            "cause": "Caused by Cercospora zeae-maydis fungus; severe in humid areas.",
            "treatment": [
                "Apply strobilurin-based fungicide (azoxystrobin) at tasseling.",
                "Plant resistant hybrid varieties.",
                "Till crop residues to reduce inoculum.",
                "Ensure adequate plant spacing.",
                "Avoid continuous corn monoculture.",
            ],
        },
        "hi": {
            "name": "मक्का – ग्रे लीफ स्पॉट",
            "cause": "Cercospora zeae-maydis; आर्द्र क्षेत्रों में गंभीर।",
            "treatment": [
                "एज़ॉक्सिस्ट्रोबिन कवकनाशी टैसलिंग पर लगाएं।",
                "प्रतिरोधी हाइब्रिड किस्में लगाएं।",
                "फसल अवशेष जोतें।",
                "पर्याप्त दूरी सुनिश्चित करें।",
                "मोनोकल्चर से बचें।",
            ],
        },
    },
    "Corn___Common_rust": {
        "en": {
            "name": "Corn – Common Rust",
            "cause": "Caused by Puccinia sorghi fungus; spreads via wind-borne spores.",
            "treatment": [
                "Apply propiconazole or azoxystrobin fungicide early.",
                "Plant rust-resistant hybrid corn varieties.",
                "Monitor fields regularly from mid-season.",
                "Avoid late planting to reduce exposure.",
                "Remove severely infected plants.",
            ],
        },
        "hi": {
            "name": "मक्का – कॉमन रस्ट",
            "cause": "Puccinia sorghi; हवा से फैलता है।",
            "treatment": [
                "प्रोपिकोनाज़ोल कवकनाशी जल्दी लगाएं।",
                "रस्ट-प्रतिरोधी हाइब्रिड मक्का लगाएं।",
                "मध्य-सीजन से नियमित निगरानी करें।",
                "देर से बुवाई से बचें।",
                "गंभीर रूप से संक्रमित पौधे हटाएं।",
            ],
        },
    },
    "Corn___Northern_Leaf_Blight": {
        "en": {
            "name": "Corn – Northern Leaf Blight (NLB)",
            "cause": "Caused by Exserohilum turcicum; large cigar-shaped lesions on leaves.",
            "treatment": [
                "Apply fungicide (azoxystrobin + propiconazole) at VT/R1 growth stage.",
                "Select NLB-resistant hybrid varieties.",
                "Practice crop rotation with non-host crops.",
                "Incorporate residue to reduce disease carryover.",
                "Ensure balanced fertilization — avoid excess nitrogen.",
            ],
        },
        "hi": {
            "name": "मक्का – नॉर्दर्न लीफ ब्लाइट",
            "cause": "Exserohilum turcicum; पत्तियों पर बड़े सिगार के आकार के धब्बे।",
            "treatment": [
                "VT/R1 स्टेज पर एज़ॉक्सिस्ट्रोबिन + प्रोपिकोनाज़ोल लगाएं।",
                "NLB-प्रतिरोधी हाइब्रिड चुनें।",
                "फसल चक्र अपनाएं।",
                "अवशेष मिट्टी में मिलाएं।",
                "संतुलित उर्वरक — अत्यधिक नाइट्रोजन से बचें।",
            ],
        },
    },
    "Corn___healthy": {
        "en": {
            "name": "Corn – Healthy",
            "cause": "No disease detected. Crop looks great!",
            "treatment": [
                "Maintain consistent irrigation, especially during silking.",
                "Apply top-dress nitrogen at V6 stage.",
                "Scout weekly for fall armyworm.",
                "Ensure proper weed management.",
                "Your corn crop is in excellent condition!",
            ],
        },
        "hi": {
            "name": "मक्का – स्वस्थ",
            "cause": "कोई बीमारी नहीं। फसल बढ़िया है!",
            "treatment": [
                "सिल्किंग के दौरान नियमित सिंचाई करें।",
                "V6 स्टेज पर यूरिया टॉप-ड्रेसिंग करें।",
                "फॉल आर्मीवर्म की साप्ताहिक जांच करें।",
                "खरपतवार प्रबंधन सुनिश्चित करें।",
                "आपकी मक्का फसल बेहतरीन स्थिति में है!",
            ],
        },
    },
}

DEFAULT_SOLUTION = {
    "en": {
        "name": "Unknown Disease",
        "cause": "The exact disease could not be determined from the image.",
        "treatment": [
            "Consult a local agricultural extension officer immediately.",
            "Take samples to your nearest Krishi Vigyan Kendra (KVK).",
            "Meanwhile, isolate affected plants from healthy ones.",
            "Avoid over-watering and ensure good drainage.",
            "Document the symptoms with photos for expert review.",
        ],
    },
    "hi": {
        "name": "अज्ञात रोग",
        "cause": "छवि से सटीक बीमारी की पहचान नहीं हो सकी।",
        "treatment": [
            "तुरंत स्थानीय कृषि अधिकारी से संपर्क करें।",
            "नजदीकी कृषि विज्ञान केंद्र (KVK) में नमूने ले जाएं।",
            "तब तक प्रभावित पौधों को अलग करें।",
            "अत्यधिक सिंचाई से बचें और जल निकासी सुनिश्चित करें।",
            "विशेषज्ञ समीक्षा के लिए लक्षणों की फोटो लें।",
        ],
    },
}


#Image Preprocessing

def preprocess_image(image_path: str) -> np.ndarray:
    """
    Load and preprocess an image for CNN inference.
    Returns a float32 numpy array of shape (1, 224, 224, 3).
    """
    img = Image.open(image_path).convert("RGB")
    img = img.resize((IMG_SIZE, IMG_SIZE), Image.LANCZOS)
    arr = np.array(img, dtype=np.float32) / 255.0   # normalise to [0, 1]
    return np.expand_dims(arr, axis=0)               # add batch dimension


def allowed_file(filename: str) -> bool:
    """Check if the uploaded file extension is allowed."""
    allowed_extensions = {"png", "jpg", "jpeg", "webp", "bmp"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


def save_uploaded_file(file_obj, filename: str) -> str:
    """
    Save an uploaded file to the /uploads directory with a timestamp prefix.
    Returns the saved file path.
    """
    import uuid
    ext       = filename.rsplit(".", 1)[1].lower()
    unique_fn = f"{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:8]}.{ext}"
    save_path = UPLOADS_DIR / unique_fn
    file_obj.save(str(save_path))
    return str(save_path)

def get_solution(class_name: str, lang: str = "en") -> dict:
    """
    Retrieve the solution dict for a given class name and language.
    Falls back to DEFAULT_SOLUTION if class not found.
    """
    lang = lang if lang in ("en", "hi") else "en"
    entry = SOLUTIONS.get(class_name, DEFAULT_SOLUTION)
    return entry.get(lang, entry.get("en", DEFAULT_SOLUTION["en"]))

def get_db_connection(config: dict):
    """
    Create and return a MySQL connection using the provided config dict.
    Config keys: host, user, password, database, port.
    """
    import mysql.connector
    conn = mysql.connector.connect(
        host     = config.get("host",     "localhost"),
        user     = config.get("user",     "root"),
        password = config.get("password", ""),
        database = config.get("database", "smart_farmer_db"),
        port     = int(config.get("port", 3306)),
    )
    return conn


def save_prediction(conn, image_path: str, disease: str,
                    confidence: float, solution: str, lang: str = "en"):
   
    cursor = conn.cursor()
    sql = """
        INSERT INTO predictions (image_path, disease, confidence, solution, language)
        VALUES (%s, %s, %s, %s, %s)
    """
    cursor.execute(sql, (image_path, disease, round(float(confidence), 4),
                         solution, lang))
    conn.commit()
    row_id = cursor.lastrowid
    cursor.close()
    return row_id


def fetch_history(conn, limit: int = 10) -> list:
    """
    Fetch the most recent `limit` predictions from the database.
    Returns a list of dicts.
    """
    cursor = conn.cursor(dictionary=True)
    cursor.execute(
        "SELECT id, image_path, disease, confidence, solution, language, created_at "
        "FROM predictions ORDER BY created_at DESC LIMIT %s",
        (limit,)
    )
    rows = cursor.fetchall()
    cursor.close()

    for row in rows:
        if hasattr(row.get("created_at"), "isoformat"):
            row["created_at"] = row["created_at"].isoformat()
    return rows
