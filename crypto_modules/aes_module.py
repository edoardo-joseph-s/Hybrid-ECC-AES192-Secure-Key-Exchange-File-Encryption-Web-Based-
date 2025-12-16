"""
AES Module for Hybrid ECC-AES192 System
Handles AES-192 encryption and decryption
"""

from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os
import time
import json
import base64

class AESManager:
    def __init__(self):
        """Initialize AES Manager"""
        self.backend = default_backend()
    
    def encrypt_file_gcm(self, file_path, aes_key, output_path=None):
        """
        Encrypt file using AES-192-GCM
        Args:
            file_path: Path to input file
            aes_key: 24-byte AES-192 key
            output_path: Path for encrypted file (optional)
        Returns:
            dict with encryption results
        """
        start_time = time.time()
        
        # Read file data
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Generate random nonce (12 bytes for GCM)
        nonce = os.urandom(12)
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.GCM(nonce),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        # Encrypt data
        encrypted_data = encryptor.update(file_data) + encryptor.finalize()
        
        # Get authentication tag
        tag = encryptor.tag
        
        # Prepare encrypted package
        encrypted_package = {
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8'),
            'ciphertext': base64.b64encode(encrypted_data).decode('utf-8'),
            'algorithm': 'AES-192-GCM',
            'original_filename': os.path.basename(file_path)
        }
        
        # Save encrypted file
        if output_path is None:
            output_path = file_path + '.enc'
        
        with open(output_path, 'w') as f:
            json.dump(encrypted_package, f, indent=2)
        
        encryption_time = time.time() - start_time
        
        return {
            'encrypted_file_path': output_path,
            'encryption_time': encryption_time,
            'original_size': len(file_data),
            'encrypted_size': len(json.dumps(encrypted_package)),
            'nonce': base64.b64encode(nonce).decode('utf-8'),
            'tag': base64.b64encode(tag).decode('utf-8'),
            'size_increase': len(json.dumps(encrypted_package)) - len(file_data),
            'size_increase_percent': ((len(json.dumps(encrypted_package)) - len(file_data)) / len(file_data)) * 100
        }
    
    def decrypt_file_gcm(self, encrypted_file_path, aes_key, output_path=None):
        """
        Decrypt file using AES-192-GCM
        Args:
            encrypted_file_path: Path to encrypted file
            aes_key: 24-byte AES-192 key
            output_path: Path for decrypted file (optional)
        Returns:
            dict with decryption results
        """
        start_time = time.time()
        
        # Load encrypted package
        with open(encrypted_file_path, 'r') as f:
            encrypted_package = json.load(f)
        
        # Extract components
        nonce = base64.b64decode(encrypted_package['nonce'])
        tag = base64.b64decode(encrypted_package['tag'])
        ciphertext = base64.b64decode(encrypted_package['ciphertext'])
        original_filename = encrypted_package.get('original_filename', 'decrypted_file')
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.GCM(nonce, tag),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        
        # Decrypt data
        try:
            decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Save decrypted file
            if output_path is None:
                output_path = original_filename
            
            with open(output_path, 'wb') as f:
                f.write(decrypted_data)
            
            decryption_time = time.time() - start_time
            
            return {
                'decrypted_file_path': output_path,
                'decryption_time': decryption_time,
                'original_encrypted_size': len(json.dumps(encrypted_package)),
                'decrypted_size': len(decrypted_data),
                'success': True,
                'error': None
            }
            
        except Exception as e:
            decryption_time = time.time() - start_time
            return {
                'decrypted_file_path': None,
                'decryption_time': decryption_time,
                'success': False,
                'error': str(e)
            }
    
    def encrypt_file_cbc(self, file_path, aes_key, output_path=None):
        """
        Encrypt file using AES-192-CBC with PKCS7 padding
        Args:
            file_path: Path to input file
            aes_key: 24-byte AES-192 key
            output_path: Path for encrypted file (optional)
        Returns:
            dict with encryption results
        """
        start_time = time.time()
        
        # Read file data
        with open(file_path, 'rb') as f:
            file_data = f.read()
        
        # Generate random IV (16 bytes for CBC)
        iv = os.urandom(16)
        
        # Apply PKCS7 padding
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(file_data) + padder.finalize()
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=self.backend
        )
        encryptor = cipher.encryptor()
        
        # Encrypt data
        encrypted_data = encryptor.update(padded_data) + encryptor.finalize()
        
        # Prepare encrypted package
        encrypted_package = {
            'iv': base64.b64encode(iv).decode('utf-8'),
            'ciphertext': base64.b64encode(encrypted_data).decode('utf-8'),
            'algorithm': 'AES-192-CBC',
            'padding': 'PKCS7',
            'original_filename': os.path.basename(file_path)
        }
        
        # Save encrypted file
        if output_path is None:
            output_path = file_path + '.enc'
        
        with open(output_path, 'w') as f:
            json.dump(encrypted_package, f, indent=2)
        
        encryption_time = time.time() - start_time
        
        return {
            'encrypted_file_path': output_path,
            'encryption_time': encryption_time,
            'original_size': len(file_data),
            'encrypted_size': len(json.dumps(encrypted_package)),
            'iv': base64.b64encode(iv).decode('utf-8'),
            'size_increase': len(json.dumps(encrypted_package)) - len(file_data),
            'size_increase_percent': ((len(json.dumps(encrypted_package)) - len(file_data)) / len(file_data)) * 100
        }
    
    def decrypt_file_cbc(self, encrypted_file_path, aes_key, output_path=None):
        """
        Decrypt file using AES-192-CBC with PKCS7 padding
        Args:
            encrypted_file_path: Path to encrypted file
            aes_key: 24-byte AES-192 key
            output_path: Path for decrypted file (optional)
        Returns:
            dict with decryption results
        """
        start_time = time.time()
        
        # Load encrypted package
        with open(encrypted_file_path, 'r') as f:
            encrypted_package = json.load(f)
        
        # Extract components
        iv = base64.b64decode(encrypted_package['iv'])
        ciphertext = base64.b64decode(encrypted_package['ciphertext'])
        original_filename = encrypted_package.get('original_filename', 'decrypted_file')
        
        # Create cipher
        cipher = Cipher(
            algorithms.AES(aes_key),
            modes.CBC(iv),
            backend=self.backend
        )
        decryptor = cipher.decryptor()
        
        # Decrypt data
        try:
            padded_data = decryptor.update(ciphertext) + decryptor.finalize()
            
            # Remove PKCS7 padding
            unpadder = padding.PKCS7(128).unpadder()
            file_data = unpadder.update(padded_data) + unpadder.finalize()
            
            # Save decrypted file
            if output_path is None:
                output_path = original_filename
            
            with open(output_path, 'wb') as f:
                f.write(file_data)
            
            decryption_time = time.time() - start_time
            
            return {
                'decrypted_file_path': output_path,
                'decryption_time': decryption_time,
                'original_encrypted_size': len(json.dumps(encrypted_package)),
                'decrypted_size': len(file_data),
                'success': True,
                'error': None
            }
            
        except Exception as e:
            decryption_time = time.time() - start_time
            return {
                'decrypted_file_path': None,
                'decryption_time': decryption_time,
                'success': False,
                'error': str(e)
            }
