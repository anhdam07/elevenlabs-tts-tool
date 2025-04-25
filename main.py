# 📦 Simple Streamlit ElevenLabs TTS Web App (User inputs API Key & Voice ID)
# ✅ Requires: streamlit, requests
# Run locally: streamlit run main.py

import streamlit as st
import requests
from io import BytesIO

# 🔐 Simple login system (hardcoded users)
USERS = {
    "user1": "1234",
    "user2": "abcd"
}

# 🧠 Simple session state login check
def login():
    st.title("🔐 ElevenLabs TTS Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.experimental_rerun()
        else:
            st.error("❌ Invalid credentials")

# 🔊 Generate voice
def generate_voice(text, api_key, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json"
    }
    payload = {
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.3,
            "similarity_boost": 0.75
        }
    }
    try:
        res = requests.post(url, headers=headers, json=payload)
        if res.status_code == 200:
            return True, res.content
        else:
            msg = res.json().get("detail", {}).get("message", f"Lỗi {res.status_code}")
            return False, msg
    except Exception as e:
        return False, str(e)

# ✅ Main app after login
def main_app():
    st.title("🎙️ ElevenLabs Text to Speech")
    st.markdown(f"👤 User: `{st.session_state['username']}`")
    st.markdown("---")

    api_key = st.text_input("🔑 Nhập API Key của bạn", type="password")
    voice_id = st.text_input("🎙️ Nhập Voice ID (hoặc để trống để dùng mặc định)")
    text = st.text_area("📝 Nhập nội dung văn bản:", height=200)

    default_voice = "EXAVITQu4vr4xnSDxMaL"  # default voice ID nếu user không nhập

    if st.button("▶️ Tạo giọng nói"):
        if not api_key or not text.strip():
            st.warning("⚠️ Vui lòng nhập API Key và văn bản.")
            return
        v_id = voice_id.strip() if voice_id.strip() else default_voice
        with st.spinner("🔄 Đang tạo giọng nói..."):
            ok, result = generate_voice(text, api_key.strip(), v_id)
            if ok:
                st.success("✅ Tạo voice thành công!")
                st.audio(result, format="audio/mp3")
                st.download_button("💾 Tải file MP3", data=BytesIO(result), file_name="voice.mp3")
            else:
                st.error(f"❌ Lỗi: {result}")

# 🚀 Start App
if "logged_in" not in st.session_state:
    login()
elif st.session_state["logged_in"]:
    main_app()
