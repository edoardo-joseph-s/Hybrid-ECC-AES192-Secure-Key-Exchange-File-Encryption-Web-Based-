KELOMPOK 7 - “Hybrid ECC–AES192: Secure Key Exchange & File Encryption”

Deskripsi Tugas
Bangun sebuah aplikasi hybrid cryptosystem yang menggabungkan:
ECC (Elliptic Curve Cryptography) sebagai algoritma asimetris untuk:
Epertukaran kunci (key agreement, misalnya ECDH), atau
enkripsi kunci simetris.
AES-192 sebagai algoritma simetris untuk enkripsi file dokumen

Aplikasi tetap berbasis upload file dan mensimulasikan skenario dua pihak (misalnya Alice dan Bob)

Tahap 1: Manajemen Kunci ECC - Generate Keypair ECC
User memilih kurva (misalnya secp256r1 atau yang didukung library).
Sistem menghasilkan pasangan public key dan private key (untuk Alice dan Bob).
Kunci disimpan dalam file format standar PEM (.pem) atau biner (.key).

Tahap 2: Key Exchange / Derivasi Shared Secret (ECDH + KDF)
Modul simulasi Alice–Bob:
Alice: Menginput Private Key miliknya dan Public Key Bob.
Bob: Menginput Private Key miliknya dan Public Key Alice.
Sistem menggunakan skema ECDH untuk menghasilkan shared secret yang sama di kedua sisi.
Alice menghitung: Shared*Point = PrivKey_A * PubKey*B.
Bob menghitung: Shared_Point = PrivKey_B * PubKey_A
Hasil Shared_Point (koordinat X, Y) di kedua sisi dijamin identik secara matematis.
Shared secret kemudian diubah menjadi kunci AES-192 melalui Key Derivation Function (KDF):
Titik koordinat hasil ECDH tidak langsung digunakan sebagai kunci.
Sistem melakukan hashing pada koordinat X dari Shared_Point menggunakan SHA-256.
Hasil hash (256 bit) dipotong (truncate) untuk mengambil 192 bit (24 byte) pertama.
Hasil Akhir: Kunci Simetris AES-192 yang valid dan aman.

Tahap 3: Enkripsi File dengan AES-192 (berbasis Shared Key ECC)
User (misalnya Alice atau bob) mengunggah file dokumen yang akan diamankan misalnya (pdf, .docx, .jpg, .zip, dll.).
Generasi IV (Initialization Vector)
Sistem secara otomatis menghasilkan IV (Initialization Vector) atau Nonce acak sepanjang 12 byte (96 bit) jika menggunakan mode GCM, atau 16 byte (128 bit) jika menggunakan mode CBC.
Catatan: IV yang unik untuk setiap file sangat krusial untuk mencegah serangan kriptoanalisis.
Sistem:
Menggunakan kunci AES-192 yang berasal dari shared secret ECC.
Mengenkripsi file menggunakan AES-192 (mode misal CBC/GCM), Direkomendasikan GCM (Galois/Counter Mode) untuk kerahasiaan dan integritas data. (Alternatif: CBC dengan PKCS#7 Padding).
Fungsi: Ciphertext, AuthTag = AES_Encrypt(Plaintext, Key_192, IV).
Hasil:
Sistem menggabungkan komponen berikut ke dalam satu file hasil enkripsi (misal: .enc):
[IV] (di bagian header file).
[Ciphertext] (isi file terenkripsi).
[Auth Tag] (jika menggunakan GCM, untuk verifikasi integritas).
Pastikan urutan byte-nya konsisten: [Panjang IV (4 byte)] + [IV (12 byte)] + [Panjang AuthTag (4 byte)] + [AuthTag (16 byte)] + [Ciphertext]
File dokumen terenkripsi
Opsi menyimpan metadata (ID kurva, info public key yang dipakai).

Tahap 4: Dekripsi File
Di sisi penerima (misalnya Bob atau Alice), user:
Mengunggah file terenkripsi (.enc).
Memasukkan/menyediakan PrivateKey_B + PublicKey_A (Memasukkan Private Key miliknya dan Public Key Alice).
Derivasi Ulang Kunci
Sistem melakukan proses ECDH + KDF yang sama seperti di Tahap 2 untuk mendapatkan kembali Kunci AES-192.
Ekstraksi Metadata
Sistem membaca file .enc dan memisahkan bagian IV, Ciphertext, dan Auth Tag.
Sistem:
Menghitung shared secret yang sama.
Menurunkan kunci AES-192 yang sama dengan mode GCM/CBC sesuai saat enkripsi).
Plaintext = AES_Decrypt(Ciphertext, Key_192, IV, AuthTag).
Mendekripsi file dan mengembalikan dokumen asli.
ika Auth Tag tidak cocok (file rusak/dimanipulasi), sistem akan menolak dekripsi.
Jika berhasil, file dokumen asli (Plaintext) dikembalikan dan dapat disimpan/dibuka oleh user.

Tahap 5: Ringkasan & Analisis
Tampilkan:
Waktu proses key agreement ECC (Lama waktu komputasi ECDH + KDF),
Waktu enkripsi–dekripsi AES-192 (Lama waktu proses AES),
Ukuran file sebelum–sesudah enkripsi (Ukuran file asli vs file terenkripsi (menunjukkan overhead dari IV dan Tag).
Mahasiswa diminta menuliskan secara singkat:
Kelebihan pendekatan hybrid ECC + AES-192 dibanding hanya RSA atau hanya AES:
Efisiensi: Kunci ECC jauh lebih kecil dari RSA untuk tingkat keamanan yang setara (256-bit ECC setara dengan 3072-bit RSA), membuat proses handshake lebih cepat dan ringan.
Kecepatan: AES sangat cepat untuk mengenkripsi data besar dibandingkan algoritma asimetris murni.
Keamanan: Menggabungkan keunggulan distribusi kunci yang aman (Asimetris) dengan kecepatan pemrosesan data (Simetris).

Output yang di harapkan:
Modul generate keypair ECC,
Modul simulasi key exchange (ECDH),
Modul enkripsi–dekripsi file menggunakan AES-192.
Penjelasan konsep ECC, ECDH, dan hubungan dengan kunci AES-192.
Diagram arsitektur alur: § generate key → key exchange → derive AES-192 → encrypt/decrypt file.
Tabel pengujian sederhana (minimal 2–3 file dengan ukuran berbeda).
