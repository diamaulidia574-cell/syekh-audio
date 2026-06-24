# 🤖 Syekh Audio: Chatbot AI Pembelajaran Maharah Istima' (Tingkat Menengah)

Proyek ini merupakan Ujian Akhir Semester (UAS) untuk mata kuliah Pembelajaran Bahasa Arab Berbasis AI. Aplikasi ini adalah sebuah chatbot interaktif berbasis terminal (CLI) yang dirancang menggunakan Python dan terintegrasi dengan Google Gemini API untuk membantu memfasilitasi pembelajaran mandiri Bahasa Arab.

---

## 👤 Identitas Mahasiswa
* **Nama:** [Dia Maulidah]
* **NIM:** [1232030156]
* **Program Studi:** Pendidikan Bahasa Arab (PBA) - Semester 6

---

## 🎯 Spesifikasi Pembelajaran
* **Fokus Maharah:** Maharah Istima' (Mendengarkan / Menyimak)
* **Target Tingkat Pengguna:** Tingkat Menengah (*Al-Mustawa al-Mutawassit*)
* **Nama Persona Chatbot:** Syekh Audio

### 💡 Alasan Pemilihan Maharah & Tingkat Pengguna
Maharah Istima' pada tingkat menengah sering kali membutuhkan variasi teks kontekstual yang lebih kaya daripada sekadar kosakata dasar. Karena keterbatasan antarmuka terminal yang berbasis teks, chatbot ini mengemas latihan menyimak melalui simulasi audio teks (seperti teks rumpang, dikte imla', dan pemahaman bacaan dialog). Tingkat menengah dipilih agar pengguna dapat memperdalam struktur kalimat (*jumlah*) dan membedakan bunyi kata (*tamyizul ashwat*) yang lebih kompleks secara interaktif tanpa kehilangan sentuhan pedagogis guru asli.

---

## 🧠 Layanan API & Teknologi Yang Digunakan
* **Language Model API:** Google Gemini API (`gemini-2.5-flash`)
* **Bahasa Pemrograman:** Python (versi 3.8 ke atas)
* **Library Utama:** 
  * `google-genai` (SDK Resmi Google Gemini)
  * `python-dotenv` (Manajemen keamanan API Key secara lokal)

---

## 🛠️ Fitur-Fitur Aplikasi
1. **Persona Konsisten (Syekh Audio):** Chatbot bertindak penuh sebagai guru yang ramah, komunikatif, menggunakan bahasa campuran Arab-Indonesia, serta rutin memberikan apresiasi/umpan balik evaluatif yang mendidik.
2. **Conversation History:** Mengingat konteks obrolan dari awal sesi hingga akhir sehingga percakapan terasa natural.
3. **Pesan Pembuka (Greeting):** Sapaan otomatis dari Syekh Audio saat program dijalankan.
4. **3 Mode Pembelajaran Khusus:**
   * **Mode 1 (Istima' wa Fahmul Masmu'):** Menyimak cerita pendek kontekstual lalu menjawab pertanyaan pemahaman.
   * **Mode 2 (Ikmalul Jumal):** Latihan melengkapi kata yang rumpang `(......)` dari kalimat yang diberikan.
   * **Mode 3 (Tamyiz al-Kalimat):** Melatih ketajaman menyimak dengan membedakan kata bermakna mirip yang makhraj hurufnya berdekatan.
5. **Navigasi Keluar Mudah:** Pengguna dapat mengetik `exit` atau `quit` kapan saja untuk kembali ke menu utama atau menutup aplikasi secara aman.

---

## 🚀 Cara Instalasi dan Menjalankan Aplikasi

### 1. Kloning Repositori
Kloning repositori GitHub ini ke komputer lokal Anda:
```bash
git clone [https://github.com/USERNAME_ANDA/NAMA_REPOSITORI.git](https://github.com/USERNAME_ANDA/NAMA_REPOSITORI.git)
cd NAMA_REPOSITORI