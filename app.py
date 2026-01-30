import streamlit as st
import requests
import json
from PIL import Image
import io

# ========== MULTILINGUAL UI TEXT ==========
UI_TEXTS = {
    "English": {
        "title": "Agri AI Assistant",
        "subtitle": "AI-powered Crop Recommendation & Disease Detection",
        "language": "Language",
        "about": "About",
        "about_text": """This AI system helps farmers:
-  Recommend best crops for soil
-  Detect plant diseases from images
-  Support 8 Indian languages
-  Works offline""",
        "tab1": " Crop Recommendation",
        "tab2": " Disease Detection",
        "crop_header": "Find the Best Crop for Your Soil",
        "soil_nutrients": " Soil Nutrients",
        "weather": " Weather Conditions",
        "nitrogen": "Nitrogen (N)",
        "phosphorus": "Phosphorus (P)",
        "potassium": "Potassium (K)",
        "temperature": "Temperature (°C)",
        "humidity": "Humidity (%)",
        "ph": "pH Level",
        "rainfall": "Rainfall (mm)",
        "crop_button": " Get Crop Recommendation",
        "analyzing": "Analyzing soil conditions...",
        "recommended": "Recommended Crop",
        "confidence": "Confidence",
        "top3": "Top 3 Recommendations",
        "disease_header": "Detect Plant Diseases from Leaf Images",
        "upload": " Upload Image",
        "upload_text": "Choose a leaf image",
        "detect": " Detect Disease",
        "camera": " Or Use Camera",
        "camera_text": "For mobile devices or webcam",
        "analyze_camera": " Analyze from Camera",
        "healthy": "🌿 Plant is Healthy!",
        "disease": "⚠️ Disease Detected",
        "other_possibilities": "🔍 Other Possibilities",
        "footer": " Agri AI Assistant - Smart Farming with AI | Snowfest Project"
    },
    "Hindi": {
        "title": " कृषि एआई सहायक",
        "subtitle": "एआई-संचालित फसल सिफारिश और रोग पहचान",
        "language": "भाषा",
        "about": "के बारे में",
        "about_text": """यह एआई सिस्टम किसानों की मदद करता है:
-  मिट्टी के लिए सर्वोत्तम फसलों की सिफारिश
-  छवियों से पौधों के रोगों का पता लगाना
-  8 भारतीय भाषाओं का समर्थन
-  ऑफलाइन काम करता है""",
        "tab1": " फसल सिफारिश",
        "tab2": " रोग पहचान",
        "crop_header": "अपनी मिट्टी के लिए सबसे अच्छी फसल खोजें",
        "soil_nutrients": " मिट्टी के पोषक तत्व",
        "weather": " मौसम की स्थिति",
        "nitrogen": "नाइट्रोजन (N)",
        "phosphorus": "फास्फोरस (P)",
        "potassium": "पोटेशियम (K)",
        "temperature": "तापमान (°C)",
        "humidity": "आर्द्रता (%)",
        "ph": "पीएच स्तर",
        "rainfall": "वर्षा (मिमी)",
        "crop_button": " फसल सिफारिश प्राप्त करें",
        "analyzing": "मिट्टी की स्थिति का विश्लेषण...",
        "recommended": "अनुशंसित फसल",
        "confidence": "विश्वास स्तर",
        "top3": "शीर्ष 3 सिफारिशें",
        "disease_header": "पत्ती की छवियों से पौधों के रोगों का पता लगाएं",
        "upload": " छवि अपलोड करें",
        "upload_text": "एक पत्ती की छवि चुनें",
        "detect": " रोग का पता लगाएं",
        "camera": " या कैमरा का उपयोग करें",
        "camera_text": "मोबाइल उपकरणों या वेबकैम के लिए",
        "analyze_camera": " कैमरा से विश्लेषण करें",
        "healthy": "🌿 पौधा स्वस्थ है!",
        "disease": "⚠️ रोग का पता चला",
        "other_possibilities": "🔍 अन्य संभावनाएं",
        "footer": " कृषि एआई सहायक - एआई के साथ स्मार्ट खेती | स्नोफेस्ट परियोजना"
    },
    "Bengali": {
        "title": " কৃষি এআই সহায়ক",
        "subtitle": "এআই-চালিত ফসল সুপারিশ এবং রোগ সনাক্তকরণ",
        "language": "ভাষা",
        "about": "সম্পর্কে",
        "about_text": """এই এআই সিস্টেম কৃষকদের সাহায্য করে:
-  মাটির জন্য সেরা ফসল সুপারিশ করে
-  চিত্র থেকে গাছের রোগ সনাক্ত করে
-  ৮টি ভারতীয় ভাষা সমর্থন করে
-  অফলাইনে কাজ করে""",
        "tab1": " ফসল সুপারিশ",
        "tab2": " রোগ সনাক্তকরণ",
        "crop_header": "আপনার মাটির জন্য সেরা ফসল খুঁজুন",
        "soil_nutrients": " মাটির পুষ্টি উপাদান",
        "weather": " আবহাওয়া অবস্থা",
        "nitrogen": "নাইট্রোজেন (N)",
        "phosphorus": "ফসফরাস (P)",
        "potassium": "পটাসিয়াম (K)",
        "temperature": "তাপমাত্রা (°C)",
        "humidity": "আর্দ্রতা (%)",
        "ph": "পিএইচ স্তর",
        "rainfall": "বৃষ্টিপাত (মিমি)",
        "crop_button": " ফসল সুপারিশ পান",
        "analyzing": "মাটির অবস্থা বিশ্লেষণ করা হচ্ছে...",
        "recommended": "সুপারিশকৃত ফসল",
        "confidence": "আত্মবিশ্বাস",
        "top3": "শীর্ষ ৩ সুপারিশ",
        "disease_header": "পাতার ছবি থেকে গাছের রোগ সনাক্ত করুন",
        "upload": " ছবি আপলোড করুন",
        "upload_text": "একটি পাতার ছবি নির্বাচন করুন",
        "detect": " রোগ সনাক্ত করুন",
        "camera": " অথবা ক্যামেরা ব্যবহার করুন",
        "camera_text": "মোবাইল ডিভাইস বা ওয়েবক্যামের জন্য",
        "analyze_camera": " ক্যামেরা থেকে বিশ্লেষণ করুন",
        "healthy": "🌿 গাছ সুস্থ!",
        "disease": "⚠️ রোগ সনাক্ত করা হয়েছে",
        "other_possibilities": "🔍 অন্যান্য সম্ভাবনা",
        "footer": " কৃষি এআই সহায়ক - এআই দিয়ে স্মার্ট চাষ | স্নোফেস্ট প্রকল্প"
    },
    "Telugu": {
        "title": " వ్యవసాయ ఎయ్‌ఐ సహాయకుడు",
        "subtitle": "ఎయ్‌ఐ-ఆధారిత పంట సిఫార్సు మరియు వ్యాధి గుర్తింపు",
        "language": "భాష",
        "about": "గురించి",
        "about_text": """ఈ ఎయ్‌ఐ సిస్టమ్ రైతులకు సహాయం చేస్తుంది:
-  నేలకు ఉత్తమ పంటలను సిఫార్సు చేస్తుంది
-  చిత్రాల నుండి మొక్కల వ్యాధులను గుర్తిస్తుంది
-  8 భారతీయ భాషలకు మద్దతు ఇస్తుంది
-  ఆఫ్‌లైన్‌లో పని చేస్తుంది""",
        "tab1": " పంట సిఫార్సు",
        "tab2": " వ్యాధి గుర్తింపు",
        "crop_header": "మీ నేలకు ఉత్తమ పంటను కనుగొనండి",
        "soil_nutrients": " నేల పోషకాలు",
        "weather": " వాతావరణ పరిస్థితులు",
        "nitrogen": "నైట్రోజన్ (N)",
        "phosphorus": "ఫాస్ఫరస్ (P)",
        "potassium": "పొటాషియం (K)",
        "temperature": "ఉష్ణోగ్రత (°C)",
        "humidity": "ఆర్ద్రత (%)",
        "ph": "పీహెచ్ స్థాయి",
        "rainfall": "వర్షపాతం (మిమీ)",
        "crop_button": " పంట సిఫార్సు పొందండి",
        "analyzing": "నేల పరిస్థితులను విశ్లేషిస్తోంది...",
        "recommended": "సిఫార్సు చేయబడిన పంట",
        "confidence": "నమ్మకం",
        "top3": "టాప్ 3 సిఫార్సులు",
        "disease_header": "ఆకు చిత్రాల నుండి మొక్కల వ్యాధులను గుర్తించండి",
        "upload": " చిత్రాన్ని అప్‌లోడ్ చేయండి",
        "upload_text": "ఒక ఆకు చిత్రాన్ని ఎంచుకోండి",
        "detect": " వ్యాధిని గుర్తించండి",
        "camera": " లేదా కెమెరాను ఉపయోగించండి",
        "camera_text": "మొబైల్ పరికరాలు లేదా వెబ్‌క్యామ్ కోసం",
        "analyze_camera": " కెమెరా నుండి విశ్లేషించండి",
        "healthy": "🌿 మొక్క ఆరోగ్యంగా ఉంది!",
        "disease": "⚠️ వ్యాధి గుర్తించబడింది",
        "other_possibilities": "🔍 ఇతర సాధ్యాలు",
        "footer": " వ్యవసాయ ఎయ్‌ఐ సహాయకుడు - ఎయ్‌ಐతో స్మಾರ್ಟ್ ವ್ಯವಸಾಯಂ | ಸ್ನೋಫೆಸ್ಟ್ ಪ್ರಾಜೆಕ್ಟ್"
    },
    "Marathi": {
        "title": " शेती एआई सहाय्यक",
        "subtitle": "एआई-चालित पीक शिफारस आणि रोग ओळख",
        "language": "भाषा",
        "about": "विषयी",
        "about_text": """ही एआई प्रणाली शेतकऱ्यांना मदत करते:
-  मातीसाठी सर्वोत्तम पिकांची शिफारस करते
-  प्रतिमांवरून वनस्पतींच्या रोगांची ओळख करते
-  ८ भारतीय भाषांना समर्थन देते
-  ऑफलाइन काम करते""",
        "tab1": " पीक शिफारस",
        "tab2": " रोग ओळख",
        "crop_header": "आपल्या मातीसाठी सर्वोत्तम पीक शोधा",
        "soil_nutrients": " मातीतील पोषकतत्वे",
        "weather": " हवामानाची परिस्थिती",
        "nitrogen": "नायट्रोजन (N)",
        "phosphorus": "फॉस्फरस (P)",
        "potassium": "पोटॅशियम (K)",
        "temperature": "तापमान (°C)",
        "humidity": "आर्द्रता (%)",
        "ph": "पीएच स्तर",
        "rainfall": "पाऊस (मिमी)",
        "crop_button": " पीक शिफारस मिळवा",
        "analyzing": "मातीच्या परिस्थितीचे विश्लेषण करीत आहे...",
        "recommended": "शिफारस केलेले पीक",
        "confidence": "आत्मविश्वास",
        "top3": "टॉप ३ शिफारसी",
        "disease_header": "पानांच्या प्रतिमांवरून वनस्पतींच्या रोगांची ओळख करा",
        "upload": " प्रतिमा अपलोड करा",
        "upload_text": "एक पानाची प्रतिमा निवडा",
        "detect": " रोग ओळखा",
        "camera": " किंवा कॅमेरा वापरा",
        "camera_text": "मोबाइल उपकरणे किंवा वेबकॅमसाठी",
        "analyze_camera": " कॅमेर्यावरून विश्लेषण करा",
        "healthy": "🌿 वनस्पती निरोगी आहे!",
        "disease": "⚠️ रोग ओळखला गेला",
        "other_possibilities": "🔍 इतर शक्यता",
        "footer": " शेती एआई सहाय्यक - एआई सह स्मार्ट शेती | स्नोफेस्ट प्रकल्प"
    },
    "Tamil": {
        "title": " விவசாய AI உதவியாளர்",
        "subtitle": "AI-இயக்கப்பட்ட பயிர் பரிந்துரை மற்றும் நோய் கண்டறிதல்",
        "language": "மொழி",
        "about": "பற்றி",
        "about_text": """இந்த AI அமைப்பு விவசாயிகளுக்கு உதவுகிறது:
-  மண்ணுக்கு சிறந்த பயிர்களை பரிந்துரைக்கிறது
-  படங்களில் இருந்து தாவர நோய்களை கண்டறியும்
-  8 இந்திய மொழிகளை ஆதரிக்கிறது
-  ஆஃப்லைனில் செயல்படுகிறது""",
        "tab1": " பயிர் பரிந்துரை",
        "tab2": " நோய் கண்டறிதல்",
        "crop_header": "உங்கள் மண்ணுக்கு சிறந்த பயிரைக் கண்டறியவும்",
        "soil_nutrients": " மண் ஊட்டச்சத்துக்கள்",
        "weather": " வானிலை நிலைமைகள்",
        "nitrogen": "நைட்ரஜன் (N)",
        "phosphorus": "பாஸ்பரஸ் (P)",
        "potassium": "பொட்டாசியம் (K)",
        "temperature": "வெப்பநிலை (°C)",
        "humidity": "ஈரப்பதம் (%)",
        "ph": "pH நிலை",
        "rainfall": "மழைப்பொழிவு (மிமீ)",
        "crop_button": " பயிர் பரிந்துரையைப் பெறுக",
        "analyzing": "மண் நிலைமைகளை பகுப்பாய்வு செய்கிறது...",
        "recommended": "பரிந்துரைக்கப்பட்ட பயிர்",
        "confidence": "நம்பிக்கை",
        "top3": "முதல் 3 பரிந்துரைகள்",
        "disease_header": "இலை படங்களில் இருந்து தாவர நோய்களைக் கண்டறியவும்",
        "upload": " படத்தைப் பதிவேற்றவும்",
        "upload_text": "ஒரு இலை படத்தைத் தேர்ந்தெடுக்கவும்",
        "detect": " நோயைக் கண்டறியவும்",
        "camera": " அல்லது கேமராவைப் பயன்படுத்தவும்",
        "camera_text": "மொபைல் சாதனங்கள் அல்லது வெப்கேம் க்கு",
        "analyze_camera": " கேமராவிலிருந்து பகுப்பாய்வு செய்யுங்கள்",
        "healthy": "🌿 தாவரம் ஆரோக்கியமாக உள்ளது!",
        "disease": "⚠️ நோய் கண்டறியப்பட்டது",
        "other_possibilities": "🔍 பிற சாத்தியக்கூறுகள்",
        "footer": " விவசாய AI உதவியாளர் - AI உடன் ஸ்மார்ட் விவசாயம் | ஸ்னோஃபெஸ்ட் திட்டம்"
    },
    "Kannada": {
        "title": " ಕೃಷಿ AI ಸಹಾಯಕ",
        "subtitle": "AI-ಚಾಲಿತ ಬೆಳೆ ಶಿಫಾರಸು ಮತ್ತು ರೋಗ ಗುರುತಿಸುವಿಕೆ",
        "language": "ಭಾಷೆ",
        "about": "ಬಗ್ಗೆ",
        "about_text": """ಈ AI ವ್ಯವಸ್ಥೆಯು ರೈತರಿಗೆ ಸಹಾಯ ಮಾಡುತ್ತದೆ:
-  ಮಣ್ಣಿಗೆ ಅತ್ಯುತ್ತಮ ಬೆಳೆಗಳನ್ನು ಶಿಫಾರಸು ಮಾಡುತ್ತದೆ
-  ಚಿತ್ರಗಳಿಂದ ಸಸ್ಯಗಳ ರೋಗಗಳನ್ನು ಗುರುತಿಸುತ್ತದೆ
-  8 ಭಾರತೀಯ ಭಾಷೆಗಳನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ
-  ಆಫ್‌ಲೈನ್‌ನಲ್ಲಿ ಕೆಲಸ ಮಾಡುತ್ತದೆ""",
        "tab1": " ಬೆಳೆ ಶಿಫಾರಸು",
        "tab2": " ರೋಗ ಗುರುತಿಸುವಿಕೆ",
        "crop_header": "ನಿಮ್ಮ ಮಣ್ಣಿಗೆ ಅತ್ಯುತ್ತಮ ಬೆಳೆಯನ್ನು ಹುಡುಕಿ",
        "soil_nutrients": " ಮಣ್ಣಿನ ಪೋಷಕಾಂಶಗಳು",
        "weather": " ಹವಾಮಾನ ಪರಿಸ್ಥಿತಿಗಳು",
        "nitrogen": "ನೈಟ್ರೊಜನ್ (N)",
        "phosphorus": "ಫಾಸ್ಫರಸ್ (P)",
        "potassium": "ಪೊಟಾಸಿಯಮ್ (K)",
        "temperature": "ತಾಪಮಾನ (°C)",
        "humidity": "ಆರ್ದ್ರತೆ (%)",
        "ph": "pH ಮಟ್ಟ",
        "rainfall": "ಮಳೆ (ಮಿಮೀ)",
        "crop_button": " ಬೆಳೆ ಶಿಫಾರಸು ಪಡೆಯಿರಿ",
        "analyzing": "ಮಣ್ಣಿನ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ವಿಶ್ಲೇಷಿಸುತ್ತಿದೆ...",
        "recommended": "ಶಿಫಾರಸು ಮಾಡಿದ ಬೆಳೆ",
        "confidence": "ನಂಬಿಕೆ",
        "top3": "ಟಾಪ್ 3 ಶಿಫಾರಸುಗಳು",
        "disease_header": "ಎಲೆ ಚಿತ್ರಗಳಿಂದ ಸಸ್ಯಗಳ ರೋಗಗಳನ್ನು ಗುರುತಿಸಿ",
        "upload": " ಚಿತ್ರವನ್ನು ಅಪ್‌ಲೋಡ್ ಮಾಡಿ",
        "upload_text": "ಒಂದು ಎಲೆಯ ಚಿತ್ರವನ್ನು ಆಯ್ಕೆಮಾಡಿ",
        "detect": " ರೋಗವನ್ನು ಗುರುತಿಸಿ",
        "camera": " ಅಥವಾ ಕ್ಯಾಮೆರಾ ಬಳಸಿ",
        "camera_text": "ಮೊಬೈಲ್ ಸಾಧನಗಳು ಅಥವಾ ವೆಬ್‌ಕ್ಯಾಮ್‌ಗಾಗಿ",
        "analyze_camera": " ಕ್ಯಾಮರಾದಿಂದ ವಿಶ್ಲೇಷಿಸಿ",
        "healthy": "🌿 ಸಸ್ಯ ಆರೋಗ್ಯವಾಗಿದೆ!",
        "disease": "⚠️ ರೋಗ ಗುರುತಿಸಲಾಗಿದೆ",
        "other_possibilities": "🔍 ಇತರ ಸಾಧ್ಯತೆಗಳು",
        "footer": " ಕೃಷಿ AI ಸಹಾಯಕ - AI ಜೊತೆ ಸ್ಮಾರ್ಟ್ ಕೃಷಿ | ಸ್ನೋಫೆಸ್ಟ್ ಪ್ರಾಜೆಕ್ಟ್"
    },
    "Punjabi": {
        "title": " ਖੇਤੀਬਾੜੀ ਏਆਈ ਸਹਾਇਕ",
        "subtitle": "ਏਆਈ-ਸੰਚਾਲਿਤ ਫਸਲ ਸਿਫਾਰਸ਼ ਅਤੇ ਰੋਗ ਦੀ ਪਛਾਣ",
        "language": "ਭਾਸ਼ਾ",
        "about": "ਬਾਰੇ",
        "about_text": """ਇਹ ਏਆਈ ਸਿਸਟਮ ਕਿਸਾਨਾਂ ਦੀ ਮਦਦ ਕਰਦਾ ਹੈ:
-  ਮਿੱਟੀ ਲਈ ਸਭ ਤੋਂ ਵਧੀਆ ਫਸਲਾਂ ਦੀ ਸਿਫਾਰਸ਼ ਕਰਦਾ ਹੈ
-  ਤਸਵੀਰਾਂ ਤੋਂ ਪੌਦਿਆਂ ਦੀਆਂ ਬੀਮਾਰੀਆਂ ਦੀ ਪਛਾਣ ਕਰਦਾ ਹੈ
-  8 ਭਾਰਤੀ ਭਾਸ਼ਾਵਾਂ ਦਾ ਸਮਰਥਨ ਕਰਦਾ ਹੈ
-  ਔਫਲਾਈਨ ਕੰਮ ਕਰਦਾ ਹੈ""",
        "tab1": " ਫਸਲ ਸਿਫਾਰਸ਼",
        "tab2": " ਰੋਗ ਦੀ ਪਛਾਣ",
        "crop_header": "ਆਪਣੀ ਮਿੱਟੀ ਲਈ ਸਭ ਤੋਂ ਵਧੀਆ ਫਸਲ ਲੱਭੋ",
        "soil_nutrients": " ਮਿੱਟੀ ਦੇ ਪੋਸ਼ਕ ਤੱਤ",
        "weather": " ਮੌਸਮ ਦੀਆਂ ਹਾਲਤਾਂ",
        "nitrogen": "ਨਾਈਟ੍ਰੋਜਨ (N)",
        "phosphorus": "ਫਾਸਫੋਰਸ (P)",
        "potassium": "ਪੋਟਾਸ਼ੀਅਮ (K)",
        "temperature": "ਤਾਪਮਾਨ (°C)",
        "humidity": "ਨਮੀ (%)",
        "ph": "ਪੀਐਚ ਪੱਧਰ",
        "rainfall": "ਬਾਰਿਸ਼ (ਮਿਮੀ)",
        "crop_button": " ਫਸਲ ਸਿਫਾਰਸ਼ ਪ੍ਰਾਪਤ ਕਰੋ",
        "analyzing": "ਮਿੱਟੀ ਦੀਆਂ ਹਾਲਤਾਂ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰ ਰਿਹਾ ਹੈ...",
        "recommended": "ਸਿਫਾਰਸ਼ੀ ਫਸਲ",
        "confidence": "ਆਤਮਵਿਸ਼ਵਾਸ",
        "top3": "ਟਾਪ 3 ਸਿਫਾਰਸ਼ਾਂ",
        "disease_header": "ਪੱਤੇ ਦੀਆਂ ਤਸਵੀਰਾਂ ਤੋਂ ਪੌਦਿਆਂ ਦੀਆਂ ਬੀਮਾਰੀਆਂ ਦੀ ਪਛਾਣ ਕਰੋ",
        "upload": " ਤਸਵੀਰ ਅੱਪਲੋਡ ਕਰੋ",
        "upload_text": "ਇੱਕ ਪੱਤੇ ਦੀ ਤਸਵੀਰ ਚੁਣੋ",
        "detect": " ਰੋਗ ਦੀ ਪਛਾਣ ਕਰੋ",
        "camera": " ਜਾਂ ਕੈਮਰੇ ਦੀ ਵਰਤੋਂ ਕਰੋ",
        "camera_text": "ਮੋਬਾਈਲ ਡਿਵਾਈਸਾਂ ਜਾਂ ਵੈਬਕੈਮ ਲਈ",
        "analyze_camera": " ਕੈਮਰੇ ਤੋਂ ਵਿਸ਼ਲੇਸ਼ਣ ਕਰੋ",
        "healthy": "🌿 ਪੌਦਾ ਸਿਹਤਮੰਦ ਹੈ!",
        "disease": "⚠️ ਰੋਗ ਦੀ ਪਛਾਣ ਹੋਈ",
        "other_possibilities": "🔍 ਹੋਰ ਸੰਭਾਵਨਾਵਾਂ",
        "footer": " ਖੇਤੀਬਾੜੀ ਏਆਈ ਸਹਾਇਕ - ਏਆਈ ਨਾਲ ਸਮਾਰਟ ਖੇਤੀਬਾੜੀ | ਸਨੋਫੈਸਟ ਪ੍ਰੋਜੈਕਟ"
    }
}

# ========== PAGE CONFIG ==========
st.set_page_config(
    page_title="Agri AI Assistant",
    page_icon="C:\\Users\\sharm\\Downloads\\Screenshot_2026-01-30_222240-removebg-preview.png",
    layout="wide"
)

# ========== ENHANCED CUSTOM CSS ==========

st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E8B57;
        text-align: center;
        margin-bottom: 1rem;
        font-weight: 700;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #228B22;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: 500;
    }
    .tab-header {
        font-size: 1.8rem;
        color: #2E8B57;
        margin-top: 1rem;
        margin-bottom: 1.5rem;
        font-weight: 600;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-size: 1.1rem;
        padding: 0.7rem 2rem;
        border-radius: 8px;
        border: none;
        font-weight: 600;
        transition: all 0.3s ease;
        margin-top: 1rem;
    }
    .stButton>button:hover {
        background-color: #3d8b40;
        transform: translateY(-2px);
    }
    .result-box {
        padding: 1.5rem;
        border-radius: 12px;
        background-color: #f8fff8;
        border: 2px solid #4CAF50;
        margin-top: 1.5rem;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    .metric-box {
        background: linear-gradient(135deg, #f0fff0, #e6ffe6);
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #c8e6c9;
        margin-bottom: 1rem;
    }
    .recommendation-item {
        padding: 0.8rem;
        margin: 0.5rem 0;
        background-color: #f9f9f9;
        border-radius: 8px;
        border-left: 4px solid #4CAF50;
    }
    .disease-name {
        font-size: 1.1rem;
        font-weight: 600;
        color: #333;
        min-width: 200px;
        word-break: break-word;
    }
    .confidence-badge {
        background-color: #e8f5e9;
        color: #2E7D32;
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.9rem;
        font-weight: 600;
    }
    .footer {
        text-align: center;
        margin-top: 3rem;
        padding: 1rem;
        color: #666;
        font-size: 0.9rem;
        border-top: 1px solid #eee;
    }
</style>
""", unsafe_allow_html=True)

# ========== IMAGE PROCESSING FUNCTION ==========
def process_image_for_api(image):
    """
    Convert any image to RGB format suitable for API
    Handles RGBA, P, L, and other modes
    """
    # Convert to RGB if needed
    if image.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', image.size, (255, 255, 255))
        
        if image.mode == 'RGBA':
            # Paste the image using alpha channel as mask
            background.paste(image, mask=image.split()[-1])
        elif image.mode == 'LA':
            # Convert LA to RGBA first
            rgba = Image.new('RGBA', image.size)
            rgba.paste(image, mask=image.split()[-1])
            background.paste(rgba, mask=rgba.split()[-1])
        elif image.mode == 'P':
            # Convert palette mode to RGB
            rgb_image = image.convert('RGB')
            return rgb_image
        
        return background
    elif image.mode != 'RGB':
        # Convert any other mode to RGB
        return image.convert('RGB')
    else:
        # Already RGB
        return image

# ========== SIDEBAR ==========

with st.sidebar:
    st.image("C:\\Users\\sharm\\Downloads\\Screenshot_2026-01-30_222240-removebg-preview.png", width=100)
    
    # Language selector
    st.markdown(f"###  {UI_TEXTS['English']['language']}")
    selected_lang = st.selectbox(
        "",
        ["English", "Hindi", "Bengali", "Telugu", "Marathi", "Tamil", "Kannada", "Punjabi"],
        label_visibility="collapsed"
    )
    
    # Get UI text for selected language
    ui = UI_TEXTS.get(selected_lang, UI_TEXTS["English"])
    
    st.markdown("---")
    st.markdown(f"###  {ui['about']}")
    st.info(ui["about_text"])

# ========== MAIN CONTENT ==========
# Title (using selected language)
st.markdown(f'<h1 class="main-header">{ui["title"]}</h1>', unsafe_allow_html=True)
st.markdown(f'<p class="sub-header">{ui["subtitle"]}</p>', unsafe_allow_html=True)

# Tabs
tab1, tab2 = st.tabs([ui["tab1"], ui["tab2"]])

with tab1:
    st.markdown(f'<h2 class="tab-header">{ui["crop_header"]}</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {ui['soil_nutrients']}")
        N = st.slider(ui["nitrogen"], 0, 140, 90)
        P = st.slider(ui["phosphorus"], 5, 145, 42)
        K = st.slider(ui["potassium"], 5, 205, 43)
    
    with col2:
        st.markdown(f"#### {ui['weather']}")
        temperature = st.slider(ui["temperature"], 8.0, 44.0, 20.87)
        humidity = st.slider(ui["humidity"], 14.0, 100.0, 82.0)
        ph = st.slider(ui["ph"], 3.5, 10.0, 6.5)
        rainfall = st.slider(ui["rainfall"], 20.0, 300.0, 202.9)
    
    if st.button(ui["crop_button"], type="primary"):
        with st.spinner(ui["analyzing"]):
            try:
                response = requests.post(
                    "http://localhost:8001/predict-crop",
                    params={
                        "N": N, "P": P, "K": K,
                        "temperature": temperature,
                        "humidity": humidity,
                        "ph": ph,
                        "rainfall": rainfall,
                        "language": selected_lang.lower()
                    }
                )
                
                if response.status_code == 200:
                    result = response.json()
                    
                    with st.container():
                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                        
                        # Main recommendation - FIXED: No double checkmark
                        col_a, col_b = st.columns([1, 2])
                        with col_a:
                            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                            st.markdown(f"**{ui['recommended']}**")
                            st.markdown(f"## {result['predicted_crop']}")
                            st.markdown('</div>', unsafe_allow_html=True)
                        with col_b:
                            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                            confidence_pct = result['confidence'] * 100
                            st.markdown(f"**{ui['confidence']}**")
                            st.markdown(f"## {confidence_pct:.1f}%")
                            st.progress(result["confidence"])
                            st.markdown('</div>', unsafe_allow_html=True)
                        
                        # Top 3 recommendations - FIXED: Better alignment
                        st.markdown(f"#### {ui['top3']}")
                        for i, pred in enumerate(result["top_3_predictions"]):
                            cols = st.columns([3, 5, 2])
                            with cols[0]:
                                # Show rank indicator
                                rank_emoji = ["🥇", "🥈", "🥉"][i]
                                st.markdown(f"{rank_emoji} **{pred['class']}**")
                            with cols[1]:
                                confidence_val = pred['confidence'] * 100
                                st.progress(pred['confidence'])
                            with cols[2]:
                                st.markdown(f'<div class="confidence-badge">{confidence_val:.1f}%</div>', unsafe_allow_html=True)
                        
                        st.markdown('</div>', unsafe_allow_html=True)
                else:
                    st.error("Failed to get prediction. Make sure FastAPI is running on port 8000.")
                    
            except Exception as e:
                st.error(f"Error: {str(e)}")

with tab2:
    st.markdown(f'<h2 class="tab-header">{ui["disease_header"]}</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown(f"#### {ui['upload']}")
        uploaded_file = st.file_uploader(ui["upload_text"], type=['jpg', 'jpeg', 'png', 'bmp', 'tiff'])
        
        if uploaded_file is not None:
            try:
                image = Image.open(uploaded_file)
                st.image(image, caption="Uploaded Image", use_column_width=True)
                
                if st.button(ui["detect"], type="primary"):
                    with st.spinner("Analyzing image..."):
                        try:
                            # FIX: Convert image to RGB BEFORE saving as JPEG
                            if image.mode in ['RGBA', 'LA', 'P']:
                                # Convert RGBA to RGB
                                rgb_image = Image.new('RGB', image.size, (255, 255, 255))
                                if image.mode == 'RGBA':
                                    rgb_image.paste(image, mask=image.split()[-1])
                                else:
                                    rgb_image.paste(image)
                                image_to_save = rgb_image
                            elif image.mode != 'RGB':
                                image_to_save = image.convert('RGB')
                            else:
                                image_to_save = image
                            
                            # Save the processed image
                            img_bytes = io.BytesIO()
                            image_to_save.save(img_bytes, format='JPEG', quality=95)
                            img_bytes.seek(0)
                            
                            # Send to API
                            files = {"file": ("image.jpg", img_bytes.getvalue(), "image/jpeg")}
                            response = requests.post(
                                "http://localhost:8001/predict-disease",
                                params={"language": selected_lang.lower()},
                                files=files
                            )
                            
                            if response.status_code == 200:
                                result = response.json()
                                
                                if 'error' in result:
                                    st.error(result['error'])
                                else:
                                    with st.container():
                                        st.markdown('<div class="result-box">', unsafe_allow_html=True)
                                        
                                        col_a, col_b = st.columns([1.5, 2])
                                        with col_a:
                                            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                                            if "Healthy" in result["predicted_disease"]:
                                                st.success(f"**{ui['healthy']}**")
                                                st.markdown(f"## Healthy")
                                            else:
                                                st.warning(f"**{ui['disease']}**")
                                                st.markdown(f"## {result['predicted_disease']}")
                                            st.markdown('</div>', unsafe_allow_html=True)
                                        with col_b:
                                            st.markdown('<div class="metric-box">', unsafe_allow_html=True)
                                            confidence_pct = result['confidence'] * 100
                                            st.markdown(f"**{ui['confidence']}**")
                                            st.markdown(f"## {confidence_pct:.1f}%")
                                            st.progress(result["confidence"])
                                            st.markdown('</div>', unsafe_allow_html=True)
                                        
                                        if len(result["top_3_predictions"]) > 1:
                                            st.markdown(f"#### {ui['other_possibilities']}")
                                            for i, pred in enumerate(result["top_3_predictions"][1:], 1):
                                                cols = st.columns([3, 5, 2])
                                                with cols[0]:
                                                    st.markdown(f'<div class="disease-name">{pred["class"]}</div>', unsafe_allow_html=True)
                                                with cols[1]:
                                                    confidence_val = pred['confidence'] * 100
                                                    st.progress(pred['confidence'])
                                                with cols[2]:
                                                    st.markdown(f'<div class="confidence-badge">{confidence_val:.1f}%</div>', unsafe_allow_html=True)
                                        
                                        st.markdown('</div>', unsafe_allow_html=True)
                            else:
                                st.error(f"Failed to detect disease. Status code: {response.status_code}")
                                
                        except Exception as e:
                            st.error(f"Error processing image: {str(e)}")
                            
            except Exception as e:
                st.error(f"Error loading image: {str(e)}")
    
    with col2:
        st.markdown(f"#### {ui['camera']}")
        st.info(ui["camera_text"])
        
        camera_image = st.camera_input("Take a photo")
        
        if camera_image:
            try:
                img = Image.open(camera_image)
                st.image(img, caption="Camera Image", use_column_width=True)
                
                if st.button(ui["analyze_camera"], type="secondary"):
                    with st.spinner("Processing camera image..."):
                        try:
                            # Process camera image the same way
                            if img.mode in ['RGBA', 'LA', 'P']:
                                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                                if img.mode == 'RGBA':
                                    rgb_img.paste(img, mask=img.split()[-1])
                                else:
                                    rgb_img.paste(img)
                                processed_img = rgb_img
                            elif img.mode != 'RGB':
                                processed_img = img.convert('RGB')
                            else:
                                processed_img = img
                            
                            img_bytes = io.BytesIO()
                            processed_img.save(img_bytes, format='JPEG', quality=95)
                            img_bytes.seek(0)
                            
                            st.info(f"Image processed successfully! Mode: {img.mode} → RGB")
                            
                        except Exception as e:
                            st.error(f"Error processing camera image: {str(e)}")
                            
            except Exception as e:
                st.error(f"Error loading camera image: {str(e)}")

# Footer
st.markdown("---")
st.markdown(f"""
<div class="footer">
    <p>{ui['footer']}</p>
</div>
""", unsafe_allow_html=True)