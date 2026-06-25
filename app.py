import os
import re
import streamlit as st
from dotenv import load_dotenv
from google import genai
from google.genai import types
from gtts import gTTS
import io

# =====================================================================
# 1. MEMUAT KONFIGURASI API KEY (.env)
# =====================================================================
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

# =====================================================================
# 2. KONFIGURASI HALAMAN WEB STREAMLIT
# =====================================================================
st.set_page_config(
    page_title="Syekh Audio - Istima' Murni Pro", 
    page_icon="🎧", 
    layout="centered"
)

st.title("👳‍♂️ Syekh Audio: Laboratorium Istima' Murni")
st.caption("Aplikasi Maharah Istima' - Dengarkan Audio untuk Menjawab Soal")

# Validasi API Key
if not api_key:
    st.error("❌ Error: GEMINI_API_KEY tidak ditemukan di file .env!")
    st.stop()

# =====================================================================
# 3. INISIALISASI GEMINI CLIENT
# =====================================================================
@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=api_key)

client = get_gemini_client()

# =====================================================================
# 4. SYSTEM PROMPT (PEMISAHAN TEKS LAYAR & TEKS AUDIO RAHASIA)
# =====================================================================
SYSTEM_PROMPT = """
Anda adalah 'Syekh Audio', tutor AI Maharah Istima' Bahasa Arab tingkat menengah.
Tugas utama Anda adalah membuat latihan menyimak di mana JAWABAN HANYA BISA DIKETAHUI JIKA SISWA MENDENGARKAN AUDIO.

Format Respon Anda HARUS SELALU mengandung dua bagian ini yang dipisahkan oleh kata kunci '[AUDIO_START]' dan '[AUDIO_END]':

Format Balasan:
<Tulis instruksi bahasa Indonesia dan pertanyaan/soal rumpang di sini untuk ditampilkan di layar web. Jangan sebutkan kata jawabannya di bagian ini! Gunakan titik-titik (......) untuk kalimat rumpang.>

[AUDIO_START]
<Tuliskan seluruh teks cerita atau kalimat UTUH dalam bahasa Arab berharakat lengkap di sini. Bagian ini AKAN DISEMBUNYIKAN dari layar dan HANYA akan diubah menjadi suara audio agar didengar siswa untuk menjawab soal di atas.>
[AUDIO_END]

Aturan Evaluasi:
Jika pengguna menjawab, periksa apakah jawabannya sesuai dengan teks audio rahasia Anda.
- Jika BENAR, sertakan kata 'MUMTAZ!' di bagian teks layar.
- Jika SALAH, sertakan kata 'COBA LAGI' di bagian teks layar.
"""

# =====================================================================
# 5. FUNGSI PEMISAH TEKS & GENERATOR AUDIO (SUDAH DIPERBAIKI)
# =====================================================================
def parse_and_generate_audio(full_text, speed_choice):
    """Fungsi memisahkan teks tampilan dan teks audio rahasia"""
    # Cari bagian di antara [AUDIO_START] dan [AUDIO_END]
    match = re.search(r'\[AUDIO_START\](.*?)\[AUDIO_END\]', full_text, re.DOTALL)
    
    display_text = full_text
    audio_text = ""
    
    if match:
        audio_text = match.group(1).strip()
        # Hapus bagian audio rahasia dari teks yang akan ditampilkan di layar
        display_text = re.sub(r'\[AUDIO_START\].*?\[AUDIO_END\]', '', full_text, flags=re.DOTALL).strip()
    
    # Jika tidak ada tag khusus, cari huruf Arab menggunakan regex standar yang aman
    if not audio_text:
        arabic_parts = re.findall(r'[\u0600-\u06FF\s]+', full_text)
        audio_text = " ".join([part.strip() for part in arabic_parts if len(part.strip()) > 3])

    if not audio_text:
        return display_text, None

    is_slow = True if speed_choice == "Slow (Lambat)" else False
    
    try:
        tts = gTTS(text=audio_text, lang='ar', slow=is_slow)
        fp = io.BytesIO()
        tts.write_to_fp(fp)
        fp.seek(0)
        return display_text, fp
    except Exception:
        return display_text, None

# =====================================================================
# 6. MENU SIDEBAR INTERAKTIF
# =====================================================================
st.sidebar.header("🏆 Papan Skor Istima'")
if "score" not in st.session_state:
    st.session_state.score = 0

st.sidebar.metric(label="Poin Anda ✨", value=f"{st.session_state.score} Poin")

if st.sidebar.button("Riset Skor 🔄"):
    st.session_state.score = 0
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("⚙️ Pengaturan Suara")
audio_speed = st.sidebar.selectbox("🔊 Kecepatan Audio:", ("Normal", "Slow (Lambat)"))

st.sidebar.markdown("---")
st.sidebar.header("📚 Pilih Jenis Latihan")
mode = st.sidebar.radio(
    "Pilih Mode Pembelajaran:",
    (
        "Obrolan Bebas / Tanya Jawab", 
        "Mode 1: Menyimak Cerita Pendek", 
        "Mode 2: Menebak Kalimat Rumpang", 
        "Mode 3: Membedakan Bunyi Mirip"
    )
)

# Inisialisasi riwayat chat
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant", 
            "content": "Assalamu'alaikum! Selamat datang di Kelas Istima' Murni! 🎧\n\nDi sini, teks jawaban tidak akan muncul di layar. Anda wajib memutar audio untuk bisa menjawab soal. Silakan pilih mode latihan di samping kiri lalu klik 'Mulai Latihan'!"
        }
    ]

# Tombol Eksekusi Pergantian Mode
if st.sidebar.button("Mulai Latihan 🚀"):
    if "Cerita Pendek" in mode:
        prompt_mode = "Mulai Mode 1: Berikan saya satu soal cerita pendek. Di teks layar berikan pertanyaan pemahamannya saja. Di dalam tag [AUDIO_START] berikan teks cerita Arab lengkapnya."
    elif "Kalimat Rumpang" in mode:
        prompt_mode = "Mulai Mode 2: Berikan saya satu kalimat rumpang (......) di teks layar. Di dalam tag [AUDIO_START] berikan kalimat UTUH versi bahasa Arabnya agar saya dengarkan kata yang hilang."
    elif "Bunyi Mirip" in mode:
        prompt_mode = "Mulai Mode 3: Berikan saya latihan membedakan bunyi mirip di teks layar (misal: tebak huruf yang benar). Di dalam tag [AUDIO_START] bunyikan kalimat Arab aslinya."
    else:
        prompt_mode = "Mari kita mengobrol santai seputar materi istima'."
        
    st.session_state.messages.append({"role": "user", "content": prompt_mode})
    
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt_mode,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.7)
    )
    st.session_state.messages.append({"role": "assistant", "content": response.text})

# =====================================================================
# 7. MENAMPILKAN PERCAKAPAN DAN KOTAK AUDIO MURNI
# =====================================================================
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] == "assistant":
            clean_text, audio_file = parse_and_generate_audio(message["content"], audio_speed)
            
            if "MUMTAZ!" in clean_text:
                st.success("🎉 JAWABAN ANDA BENAR!")
            elif "COBA LAGI" in clean_text:
                st.warning("⚠️ JAWABAN KURANG TEPAT, YUK COBA LAGI!")
                
            st.write(clean_text)
            
            if audio_file:
                st.markdown("🎧 **Dengarkan Audio ini untuk menjawab:**")
                st.audio(audio_file, format='audio/mp3')
        else:
            st.write(message["content"])

# =====================================================================
# 8. KOLOM INPUT PENGGUNA & LOGIKA FEEDBACK
# =====================================================================
if user_input := st.chat_input("Ketik jawaban Anda di sini..."):
    with st.chat_message("user"):
        st.write(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    formatted_history = [
        types.Content(
            role="user" if m["role"] == "user" else "model", 
            parts=[types.Part.from_text(text=m["content"])]
        )
        for m in st.session_state.messages
    ]

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=formatted_history,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.7)
    )

    if "MUMTAZ!" in response.text:
        st.session_state.score += 1
        st.balloons()

    st.session_state.messages.append({"role": "assistant", "content": response.text})
    st.rerun() 