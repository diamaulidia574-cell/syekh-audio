import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

# 1. Memuat konfigurasi API Key dari file .env
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("Error: GEMINI_API_KEY tidak ditemukan di file .env!")
    exit(1)

# 2. Inisialisasi Google Gemini Client
client = genai.Client(api_key=api_key)

# 3. Definisikan System Prompt untuk Persona "Syekh Audio"
SYSTEM_PROMPT = """
Anda adalah 'Syekh Audio', seorang tutor AI ahli dalam pembelajaran Maharah Istima' (Mendengarkan) Bahasa Arab untuk tingkat menengah (Al-Mustawa al-Mutawassit). 

Tugas Anda adalah melatih kepekaan pemahaman teks yang diasumsikan sebagai audio lewat terminal interaktif teks ini.

Karakteristik Anda:
1. Selalu menyapa di awal dengan ramah menggunakan bahasa Arab fusha yang jelas dicampur instruksi bahasa Indonesia.
2. Fokus pada kosakata tingkat menengah (Tema: Lingkungan, Kesehatan, Pendidikan, atau Perjalanan).
3. Anda harus memandu pengguna sesuai dengan "Mode" yang mereka pilih di menu utama.
4. Evaluasi jawaban pengguna dengan sabar. Jika salah, berikan petunjuk (clue) halus, jangan langsung membongkar jawaban benarnya.
5. Berikan apresiasi seperti 'Ahsanta!', 'Mumtaz!', atau 'Barakallahu feek' jika pengguna menjawab dengan benar.

Ingat, selalu gunakan persona 'Syekh Audio' dan jangan pernah keluar dari karakter ini.
"""

def main():
    print("====================================================")
    print("🤖 SYEKH AUDIO - Chatbot Maharah Istima' (Menengah) 🤖")
    print("====================================================")
    print("Ketik 'exit' atau 'quit' untuk kembali ke menu/keluar.\n")

    # 4. Inisialisasi Chat dengan System Instruction (Fitur History Otomatis)
    # Kita menggunakan model 'gemini-2.5-flash' yang cepat dan optimal untuk teks
    chat = client.chats.create(
        model="gemini-2.5-flash",
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.7,
        )
    )

    # Kirim sapaan pembuka otomatis dari AI (Greeting)
    welcome_msg = chat.send_message("Kirimkan salam pembuka (greeting) hangat sebagai Syekh Audio dan tanyakan kesiapan belajar pengguna.")
    print(f"\nSyekh Audio: {welcome_msg.text}\n")

    while True:
        print("--- PILIHAN MODE BELAJAR ---")
        print("1. Mode 1: Istima' wa Fahmul Masmu' (Menyimak & Memahami Cerita)")
        print("2. Mode 2: Ikmalul Jumal (Melengkapi Kalimat Rumpang)")
        print("3. Mode 3: Tamyiz al-Kalimat (Membedakan Bunyi Kata Mirip)")
        print("4. Keluar dari Aplikasi")
        print("----------------------------")
        
        pilihan = input("Pilih nomor mode yang ingin Anda mainkan (1-4): ").strip()

        if pilihan == '4' or pilihan.lower() in ['exit', 'quit']:
            print("\nSyekh Audio: Ilalliqo! Ma'as salamah... Semoga ilmu kita bermanfaat!")
            break
        
        elif pilihan == '1':
            prompt_mode = "Mulai Mode 1: Berikan saya satu cerita pendek tingkat menengah. Setelah saya baca, berikan pertanyaan pemahamannya."
        elif pilihan == '2':
            prompt_mode = "Mulai Mode 2: Berikan saya latihan teks rumpang tingkat menengah dengan tanda (......) untuk saya tebak katanya."
        elif pilihan == '3':
            prompt_mode = "Mulai Mode 3: Berikan saya latihan membedakan dua bunyi kata yang mirip dalam konteks kalimat tingkat menengah."
        else:
            print("\nPilihan tidak valid. Silakan pilih nomor 1 sampai 4.\n")
            continue

        # Kirim perintah instruksi mode ke Gemini API
        response = chat.send_message(prompt_mode)
        print(f"\nSyekh Audio: {response.text}\n")

        # Loop Percakapan Interaktif di dalam Mode yang dipilih
        while True:
            user_input = input("Jawaban / Respon Anda: ").strip()
            
            if user_input.lower() in ['exit', 'quit']:
                print("\n[Kembali ke Menu Utama]\n")
                break
                
            # Mengirimkan chat pengguna dan mendapatkan balasan yang mengingat riwayat sebelumnya
            response = chat.send_message(user_input)
            print(f"\nSyekh Audio: {response.text}\n")

if __name__ == "__main__":
    main()
