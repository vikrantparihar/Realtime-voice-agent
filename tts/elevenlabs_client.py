import os
import requests
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------
# CONFIG
# -----------------------------------

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("ELEVENLABS_VOICE_ID")

if not ELEVENLABS_API_KEY:
    raise Exception("ELEVENLABS_API_KEY missing")

if not VOICE_ID:
    raise Exception("ELEVENLABS_VOICE_ID missing")


# -----------------------------------
# TTS GENERATION (FINAL FIXED)
# -----------------------------------

def generate_speech(text: str):

    try:
        if not text or not text.strip():
            return None

        url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}"

        headers = {
            "xi-api-key": ELEVENLABS_API_KEY,
            "Content-Type": "application/json"
        }

        payload = {
            "text": text,

            # 🔥 FIX: working model (no free-tier break)
            "model_id": "eleven_turbo_v2_5",

            "voice_settings": {
                "stability": 0.4,
                "similarity_boost": 0.75
            }
        }

        response = requests.post(
            url,
            json=payload,
            headers=headers,
            timeout=20
        )

        if response.status_code == 200:
            return response.content

        print("❌ ELEVENLABS ERROR:", response.status_code)
        print(response.text)
        return None

    except Exception as e:
        print("TTS ERROR:", e)
        return None