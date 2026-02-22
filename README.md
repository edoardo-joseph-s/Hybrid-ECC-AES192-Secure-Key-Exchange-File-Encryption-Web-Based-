# Hybrid ECC-AES192 Secure Key Exchange & File Encryption (Web-Based)

Aplikasi web berbasis Flask untuk demonstrasi kriptografi hibrid:
- Pertukaran kunci menggunakan `ECC + ECDH`
- Derivasi kunci simetris menggunakan `HKDF-SHA256`
- Enkripsi/dekripsi file menggunakan `AES-192` (mode `GCM` atau `CBC`)

Project ini ditujukan untuk kebutuhan edukasi/akademik, bukan langsung untuk produksi.

## Fitur Utama

- Generate keypair ECC untuk dua pihak (Alice dan Bob) dengan kurva `secp256r1`
- Verifikasi hasil pertukaran kunci ECDH (shared secret dan kunci AES harus cocok)
- Enkripsi file dengan:
  - `AES-192-GCM` (direkomendasikan)
  - `AES-192-CBC` (dengan PKCS7 padding)
- Dekripsi file terenkripsi berdasarkan metadata algoritma dalam file `.enc`
- Download hasil file terenkripsi/dekripsi dari web UI
- Log performa operasi (key generation, key exchange, encrypt, decrypt)
- Batas ukuran upload file: `16 MB`

## Stack

- Python 3
- Flask `2.3.3`
- cryptography `41.0.7`
- Werkzeug `2.3.7`
- Frontend: HTML + CSS + JavaScript (Bootstrap 5, jQuery)

## Struktur Project

```text
.
├── app.py
├── requirements.txt
├── crypto_modules/
│   ├── __init__.py
│   ├── ecc_module.py
│   ├── ecdh_module.py
│   └── aes_module.py
├── templates/
│   └── index.html
└── static/
    ├── css/
    │   ├── main.css
    │   └── process.css
    └── js/
        ├── main.js
        └── process.js
```

Saat aplikasi berjalan, folder berikut akan otomatis dibuat jika belum ada:
- `uploads/`
- `keys/`
- `encrypted/`

## Alur Kriptografi

1. Generate pasangan kunci ECC Alice dan Bob (`secp256r1`).
2. Lakukan ECDH untuk menghasilkan shared secret di kedua sisi.
3. Derivasi kunci `AES-192` (24 byte) dari shared secret dengan HKDF-SHA256.
4. Gunakan kunci AES hasil derivasi untuk enkripsi/dekripsi file.

## Instalasi & Menjalankan

1. Buat virtual environment (opsional tapi direkomendasikan):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install dependency:

```bash
pip install -r requirements.txt
```

3. Jalankan aplikasi:

```bash
python app.py
```

4. Buka di browser:

```text
http://localhost:5002
```

## Cara Pakai (UI)

1. `Generate`: klik **Buat Keypair**
2. `Exchange`: klik **Lakukan Pertukaran Kunci**
3. `Encrypt`: pilih file, pilih mode (`GCM`/`CBC`), klik **Enkripsi File**
4. `Decrypt`: upload file `.enc`, klik **Dekripsi File**
5. Gunakan tombol download untuk mengambil hasil enkripsi/dekripsi
6. Gunakan **Reset Sistem** untuk menghapus state dan file sementara

## Endpoint API

- `GET /`  
  Halaman utama.

- `GET /generate_keys`  
  Generate kunci ECC Alice/Bob.

- `GET /key_exchange`  
  Menjalankan ECDH + HKDF dan verifikasi kecocokan kunci.

- `POST /encrypt_file`  
  Enkripsi file. Form-data:
  - `file`: file input
  - `mode`: `gcm` (default) atau `cbc`

- `POST /decrypt_file`  
  Dekripsi file terenkripsi (`.enc` JSON package).

- `GET /download_file/<filename>`  
  Download file hasil proses.

- `GET /performance`  
  Ambil log dan statistik performa.

- `GET /reset`  
  Reset session in-memory + pembersihan file sementara.

## Format File Enkripsi

Output enkripsi disimpan sebagai JSON, berisi metadata seperti:
- `algorithm`
- `original_filename`
- `ciphertext` (Base64)
- `nonce` + `tag` (untuk GCM) atau `iv` (untuk CBC)

Ekstensi output default: `.enc`

## Catatan Keamanan

- Aplikasi berjalan dengan `debug=True` (hanya untuk development).
- `secret_key` Flask diset statis di source code.
- Manajemen sesi masih in-memory global (`session_data`) dan belum cocok untuk multi-user production.
- Kunci privat disimpan ke file PEM tanpa passphrase.

Untuk penggunaan produksi, perlu hardening tambahan (secret management, session store, authN/authZ, secure key storage, TLS, logging sanitization, dsb).

## Lisensi

Belum ditentukan. Tambahkan file `LICENSE` sesuai kebutuhan Anda.
