TECHNICAL DOCUMENT
Hybrid ECC–AES192: Secure Key Exchange & File Encryption (Web-Based)
1. Tujuan Sistem
Membangun aplikasi web yang mengimplementasikan hybrid cryptosystem dengan:
ECC (ECDH) untuk pertukaran kunci secara aman
AES-192 untuk enkripsi dan dekripsi file dokumen
Aplikasi mensimulasikan komunikasi aman antara dua pihak (Alice & Bob) melalui mekanisme upload file dan pertukaran public key.
2. Arsitektur Sistem
2.1 Arsitektur Umum
Aplikasi menggunakan arsitektur client–server berbasis web:
Client (Browser)
│
│ Upload file, upload key, download hasil
│
▼
Web Server (Backend Python)
│
├─ ECC Key Management Module
├─ ECDH Key Exchange Module
├─ AES-192 Encryption Module
├─ AES-192 Decryption Module
├─ Performance Measurement Module
│
▼
File Storage (Encrypted & Decrypted Files)
2.2 Komponen Sistem
Komponen	Deskripsi
Frontend	Antarmuka web untuk upload file & key
Backend	Logika kriptografi ECC & AES
Crypto Engine	Implementasi ECDH, HKDF, AES-192
Storage	Penyimpanan key & file
Logger	Pengukuran waktu & ukuran file
3. Teknologi yang Digunakan
3.1 Platform & Bahasa
Backend: Python 3.x
Web Framework: Flask / FastAPI
Frontend: HTML, CSS, Bootstrap
Server: Localhost / Web Server
3.2 Library Kriptografi
Library	Fungsi
cryptography	ECC, ECDH, HKDF, AES
os	Manajemen file
time	Pengukuran performa
base64	Encoding data
hashlib	Hash tambahan (opsional)
4. Desain Modul Sistem
4.1 Modul Generate Keypair ECC
Fungsi
Menghasilkan pasangan Private Key & Public Key ECC untuk Alice dan Bob.
Proses
User memilih kurva ECC (secp256r1)
Sistem menghasilkan keypair ECC
Key disimpan dalam format .pem
Output
alice_private.pem
alice_public.pem
bob_private.pem
bob_public.pem
4.2 Modul Key Exchange (ECDH)
Fungsi
Menghasilkan shared secret yang sama di sisi Alice dan Bob.
Proses
Alice:
Input: PrivateKey_A + PublicKey_B
Bob:
Input: PrivateKey_B + PublicKey_A
Sistem menjalankan ECDH
Output
Shared Secret (byte array)
📌 Catatan: Shared secret tidak disimpan, hanya dipakai untuk derivasi kunci.
4.3 Modul Key Derivation (AES-192)
Fungsi
Mengubah shared secret menjadi kunci AES-192 (192-bit)
Metode
HKDF (HMAC-based Key Derivation Function)
Output: 24 byte (192 bit)
Parameter
Hash: SHA-256
Salt: opsional
Info: "AES-192-Key"
4.4 Modul Enkripsi File (AES-192)
Fungsi
Mengenkripsi file dokumen menggunakan AES-192
Mode
AES-192-GCM (direkomendasikan)
atau
AES-192-CBC + Padding
Proses
User upload file
Sistem generate IV / nonce
File dienkripsi
Metadata disimpan
Output
File terenkripsi (.enc)
Metadata:
Kurva ECC
IV / Nonce
Public Key pengirim
4.5 Modul Dekripsi File
Fungsi
Mengembalikan file asli dari file terenkripsi.
Input
File terenkripsi
PrivateKey_B
PublicKey_A
Proses
Hitung shared secret via ECDH
Derivasi kunci AES-192
Dekripsi file
Output
File asli (plaintext)
4.6 Modul Analisis & Logging
Fungsi
Mencatat performa sistem.
Parameter yang Dicatat
Waktu ECDH
Waktu enkripsi AES-192
Waktu dekripsi AES-192
Ukuran file sebelum & sesudah enkripsi
Output
Tabel pengujian
Data analisis untuk laporan
5. Alur Sistem (Flow Sistem)
5.1 Enkripsi (Alice)
Generate Key ECC
     ↓
Exchange Public Key
     ↓
ECDH → Shared Secret
     ↓
HKDF → AES-192 Key
     ↓
Encrypt File (AES-192)
     ↓
Encrypted File
5.2 Dekripsi (Bob)
Upload Encrypted File
     ↓
ECDH (Private_B + Public_A)
     ↓
Shared Secret
     ↓
HKDF → AES-192 Key
     ↓
Decrypt File
     ↓
Original File
6. Keamanan Sistem
Aspek	Penjelasan
Key Confidentiality	Private key tidak pernah dikirim
Forward Secrecy	Shared secret tidak disimpan
Data Confidentiality	File dienkripsi AES-192
Integrity (GCM)	Tag autentikasi memastikan file tidak diubah
7. Kelebihan Hybrid ECC–AES192
ECC:
Ukuran kunci kecil
Proses cepat
Aman
AES-192:
Sangat cepat untuk file besar
Hybrid:
ECC aman untuk pertukaran kunci
AES efisien untuk enkripsi data
Lebih baik dari RSA-only atau AES-only
8. Batasan Sistem
Simulasi dua pihak (Alice & Bob)
Tidak menggunakan sertifikat digital
Belum mendukung multi-user
Fokus akademik, bukan produksi
9. Pengembangan Lanjutan
Integrasi GUI modern (React/Vue)
Penyimpanan key terenkripsi
Multi-user session
Penambahan digital signature (ECDSA)