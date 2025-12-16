# Hybrid ECC-AES192: Secure Key Exchange & File Encryption (Web-Based)

A web-based application demonstrating hybrid cryptosystem combining Elliptic Curve Cryptography (ECC) with Advanced Encryption Standard (AES-192) for secure key exchange and file encryption.

## 🛡️ Overview

This application simulates secure communication between two parties (Alice and Bob) using:
- **ECC (secp256r1)** for key generation and exchange
- **ECDH** for secure key agreement
- **HKDF** for AES-192 key derivation
- **AES-192** for symmetric file encryption (GCM/CBC modes)

## 🚀 Features

### Core Functionality
- ✅ ECC keypair generation for Alice and Bob
- ✅ ECDH key exchange with performance measurement
- ✅ HKDF-based AES-192 key derivation
- ✅ File encryption (AES-192-GCM and AES-192-CBC)
- ✅ File decryption with integrity verification
- ✅ Real-time performance analysis and logging

### Security Features
- 🔐 Forward secrecy through ECDH
- 🔒 Authentication via GCM mode
- 🗝️ Secure key derivation with HKDF-SHA256
- 🚫 No private key transmission
- 📊 Performance monitoring and analysis

### User Interface
- 🎨 Modern responsive web interface
- 📱 Mobile-friendly design
- 📈 Real-time performance metrics
- 💾 File download functionality
- 🔄 System reset capabilities

## 📋 Prerequisites

- Python 3.8+
- pip package manager

## 🛠️ Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd hybrid-ecc-aes192
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application:**
   ```bash
   python app.py
   ```

4. **Access the application:**
   Open your web browser and navigate to `http://localhost:5000`

## 📁 Project Structure

```
hybrid-ecc-aes192/
├── app.py                          # Flask web application
├── requirements.txt                 # Python dependencies
├── crypto_modules/                  # Cryptography modules
│   ├── __init__.py
│   ├── ecc_module.py              # ECC key management
│   ├── ecdh_module.py            # ECDH key exchange
│   └── aes_module.py             # AES-192 encryption/decryption
├── templates/
│   └── index.html                 # Web interface
├── uploads/                       # Temporary file storage
├── keys/                         # Generated key files
├── encrypted/                     # Encrypted files
├── tecnical_document.md           # Technical specifications
├── srs.md                        # Software requirements
└── README.md                     # This file
```

## 🔧 Usage Guide

### Step 1: Generate ECC Keys
1. Click "Generate Keys" button
2. System generates keypairs for Alice and Bob using secp256r1 curve
3. Public keys are displayed, private keys are stored securely

### Step 2: Perform Key Exchange
1. Click "Exchange Keys" button
2. System performs ECDH key exchange
3. AES-192 key is derived using HKDF
4. Performance metrics are displayed

### Step 3: Encrypt File
1. Choose a file to encrypt (max 16MB)
2. Select encryption mode (GCM recommended)
3. Click "Encrypt File"
4. Download encrypted file

### Step 4: Decrypt File
1. Upload the encrypted file
2. Click "Decrypt File"
3. Download the decrypted file
4. Verify file integrity

## 🔐 Security Implementation

### ECC Component
- **Curve**: secp256r1 (prime256v1)
- **Key Size**: 256-bit private key, 256-bit public key
- **Algorithm**: Elliptic Curve Digital Signature Algorithm (ECDSA)

### ECDH Key Exchange
- **Protocol**: Elliptic Curve Diffie-Hellman
- **Shared Secret**: 256-bit (32 bytes)
- **Security**: Forward secrecy, no key transmission

### HKDF Key Derivation
- **Hash Function**: SHA-256
- **Output Length**: 192 bits (24 bytes) for AES-192
- **Info**: "AES-192-Key" for context
- **Salt**: Zero salt for consistency

### AES-192 Encryption
- **Key Size**: 192 bits (24 bytes)
- **Block Size**: 128 bits
- **Modes**: GCM (recommended) and CBC
- **Authentication**: GCM provides integrity, CBC with PKCS7 padding

## 📊 Performance Analysis

The system tracks and analyzes:
- **Key Generation Time**: Time to generate ECC keypairs
- **Key Exchange Time**: ECDH computation and HKDF derivation
- **Encryption Time**: File encryption duration
- **Decryption Time**: File decryption duration
- **File Size Analysis**: Original vs encrypted file sizes
- **Throughput**: Encryption/decryption speed metrics

## 🧪 Testing

### Manual Testing
1. Start the application: `python app.py`
2. Open browser to `http://localhost:5000`
3. Follow the 4-step process
4. Verify file encryption/decryption
5. Check performance metrics

### Automated Testing
```python
# Test key generation
python -c "
from crypto_modules import ECCManager
ecc = ECCManager()
keys = ecc.generate_keypair('test')
print('Keys generated successfully')
"

# Test encryption
python -c "
from crypto_modules import AESManager
aes = AESManager()
with open('test.txt', 'w') as f: f.write('Hello World')
result = aes.encrypt_file_gcm('test.txt', b'24-byte-key-for-testing!!')
print('Encryption successful')
"
```

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Development/production mode
- `MAX_CONTENT_LENGTH`: Maximum file upload size (default: 16MB)

### File Limits
- **Maximum File Size**: 16MB
- **Supported File Types**: All file types
- **Storage**: Temporary (cleared on reset)

## 🐛 Troubleshooting

### Common Issues

1. **Import Errors**:
   ```bash
   pip install --upgrade cryptography flask werkzeug
   ```

2. **File Upload Issues**:
   - Check file size limit (16MB)
   - Ensure permissions on upload directories

3. **Key Generation Failures**:
   - Verify cryptography library installation
   - Check system entropy for key generation

4. **Performance Issues**:
   - Monitor system resources
   - Check file sizes for encryption/decryption

### Debug Mode
Enable debug mode for detailed error messages:
```python
app.run(debug=True)
```

## 📈 Performance Benchmarks

Typical performance on modern hardware:

| Operation | Time (seconds) |
|------------|----------------|
| ECC Key Generation | 0.001-0.005 |
| ECDH Exchange | 0.002-0.008 |
| HKDF Derivation | 0.0001-0.001 |
| AES-192 Encryption (1MB) | 0.01-0.05 |
| AES-192 Decryption (1MB) | 0.01-0.05 |

## 🔒 Security Considerations

### Implemented Security Measures
- Private keys never transmitted
- Forward secrecy through ECDH
- Authentication via GCM mode
- Secure key derivation with HKDF
- No persistent storage of shared secrets

### Limitations (Educational Use)
- Single session (no multi-user support)
- No certificate-based authentication
- Temporary file storage
- Basic session management

### Production Recommendations
- Implement proper session management
- Add user authentication
- Use secure key storage
- Implement certificate validation
- Add audit logging
- Use production-ready web server

## 📚 Technical References

- [NIST FIPS 197 - Advanced Encryption Standard](https://csrc.nist.gov/publications/fips/fips197/final)
- [NIST SP 800-56A - Key Establishment using ECC](https://csrc.nist.gov/publications/detail/sp/800-56a/rev-3/final)
- [RFC 5869 - HMAC-based Key Derivation Function (HKDF)](https://tools.ietf.org/html/rfc5869)
- [Python Cryptography Documentation](https://cryptography.io/en/latest/)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

This project is for educational purposes. Please refer to the license file for usage terms.

## 👥 Authors

- **Developer**: [Your Name]
- **Project**: Hybrid ECC-AES192 Cryptography System

## 📞 Support

For questions or issues:
1. Check the troubleshooting section
2. Review technical documentation
3. Create an issue with detailed information

---

**⚠️ Important**: This is an educational demonstration. For production cryptographic systems, consult with security experts and use established cryptographic libraries with proper security audits.
