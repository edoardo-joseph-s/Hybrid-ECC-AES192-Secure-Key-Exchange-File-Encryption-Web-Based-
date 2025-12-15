SOFTWARE REQUIREMENTS SPECIFICATION (SRS)
Hybrid ECC–AES192: Secure Key Exchange & File Encryption (Web-Based Application)
1. Pendahuluan
1.1 Tujuan Dokumen
Dokumen Software Requirements Specification (SRS) ini bertujuan untuk mendefinisikan secara rinci kebutuhan perangkat lunak dari aplikasi Hybrid ECC–AES192 yang mengimplementasikan:
Elliptic Curve Cryptography (ECC) untuk pertukaran kunci menggunakan ECDH
AES-192 untuk enkripsi dan dekripsi file dokumen
Dokumen ini menjadi acuan bagi proses perancangan, implementasi, pengujian, dan evaluasi sistem.
1.2 Ruang Lingkup Sistem
Aplikasi yang dibangun adalah aplikasi berbasis web yang:
Mensimulasikan komunikasi aman antara dua pihak (Alice dan Bob)
Menggunakan mekanisme hybrid cryptosystem
Mendukung upload file, enkripsi, dan dekripsi
Menampilkan hasil analisis performa kriptografi
1.3 Definisi, Akronim, dan Singkatan
Istilah	Deskripsi
ECC	Elliptic Curve Cryptography
ECDH	Elliptic Curve Diffie-Hellman
AES-192	Advanced Encryption Standard 192-bit
Shared Secret	Nilai rahasia hasil ECDH
KDF	Key Derivation Function
HKDF	HMAC-based Key Derivation Function
IV	Initialization Vector
GCM	Galois/Counter Mode
1.4 Referensi
NIST FIPS 197 – Advanced Encryption Standard
NIST SP 800-56A – Recommendation for Pair-Wise Key-Establishment Using ECC
RFC 5869 – HMAC-based Key Derivation Function (HKDF)
Python Cryptography Documentation
2. Deskripsi Umum Sistem
2.1 Perspektif Produk
Aplikasi ini merupakan sistem mandiri (standalone web application) yang berjalan di browser dan server backend Python. Sistem tidak terintegrasi dengan layanan eksternal.
2.2 Fungsi Sistem
Fungsi utama sistem meliputi:
Generate keypair ECC
Simulasi pertukaran kunci (ECDH)
Derivasi kunci AES-192
Enkripsi file dokumen
Dekripsi file dokumen
Analisis performa kriptografi
2.3 Karakteristik Pengguna
Pengguna	Deskripsi
User	Mahasiswa / pengguna aplikasi untuk simulasi kriptografi
2.4 Batasan Sistem
Sistem hanya mendukung satu kurva ECC (misalnya secp256r1)
Sistem tidak menggunakan sertifikat digital
Tidak mendukung multi-user authentication
Digunakan untuk keperluan akademik
3. Kebutuhan Fungsional (Functional Requirements)
FR-1: Generate Keypair ECC
Sistem harus menyediakan fitur untuk menghasilkan pasangan kunci ECC (private key dan public key).
Deskripsi:
User memilih kurva ECC
Sistem menghasilkan keypair ECC untuk Alice dan Bob
Kunci disimpan dalam format file (.pem)
FR-2: Pertukaran Kunci (ECDH)
Sistem harus mampu menghasilkan shared secret yang sama melalui skema ECDH.
Deskripsi:
Alice menggunakan PrivateKey_A dan PublicKey_B
Bob menggunakan PrivateKey_B dan PublicKey_A
Sistem menghitung shared secret di kedua sisi
FR-3: Derivasi Kunci AES-192
Sistem harus menurunkan kunci AES-192 dari shared secret ECC.
Deskripsi:
Sistem menggunakan KDF (HKDF)
Output berupa kunci simetris 192-bit
FR-4: Enkripsi File
Sistem harus dapat mengenkripsi file dokumen menggunakan AES-192.
Deskripsi:
User mengunggah file
Sistem mengenkripsi file menggunakan AES-192 (CBC/GCM)
Sistem menghasilkan file terenkripsi dan metadata
FR-5: Dekripsi File
Sistem harus dapat mendekripsi file terenkripsi menjadi file asli.
Deskripsi:
User mengunggah file terenkripsi
User menyediakan PrivateKey_B dan PublicKey_A
Sistem mendekripsi file menggunakan kunci AES-192 yang sama
FR-6: Analisis & Logging
Sistem harus menampilkan hasil analisis performa.
Deskripsi:
Waktu key agreement ECC
Waktu enkripsi dan dekripsi AES-192
Ukuran file sebelum dan sesudah enkripsi
4. Kebutuhan Non-Fungsional (Non-Functional Requirements)
NFR-1: Keamanan
Private key tidak boleh dikirim ke pihak lain
Shared secret tidak disimpan secara permanen
AES menggunakan IV/nonce unik
NFR-2: Performa
Proses ECDH harus selesai dalam waktu < 1 detik untuk file kecil
Enkripsi dan dekripsi file berjalan secara efisien
NFR-3: Usability
Antarmuka web sederhana dan mudah dipahami
Proses upload dan download file jelas
NFR-4: Portabilitas
Aplikasi dapat dijalankan pada OS Windows, Linux, dan macOS
Berjalan pada browser modern
NFR-5: Maintainability
Struktur kode modular
Mudah dikembangkan untuk fitur tambahan
5. Use Case Diagram (Deskriptif)
Use Case Utama
Generate ECC Keypair
Exchange Public Key
Encrypt File
Decrypt File
View Analysis Result
6. Asumsi dan Ketergantungan
Asumsi
User memahami konsep dasar kriptografi
File yang dienkripsi tidak rusak
Ketergantungan
Library Python cryptography
Web framework Python (Flask/FastAPI)
7. Kriteria Keberhasilan Sistem
Sistem dianggap berhasil jika:
File dapat dienkripsi dan didekripsi dengan benar
Shared secret di Alice dan Bob identik
Kunci AES-192 konsisten
Hasil analisis ditampilkan sesuai spesifikasi
8. Penutup
Dokumen SRS ini menjadi dasar pengembangan aplikasi Hybrid ECC–AES192 dan memastikan bahwa sistem yang dibangun memenuhi kebutuhan fungsional dan non-fungsional sesuai dengan spesifikasi tugas.