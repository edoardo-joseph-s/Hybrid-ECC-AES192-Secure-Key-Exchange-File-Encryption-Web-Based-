"""
ECC Module for Hybrid ECC-AES192 System
Handles ECC key generation and management
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os
import time

class ECCManager:
    def __init__(self, curve=ec.SECP256R1()):
        """
        Initialize ECC Manager with specified curve
        Default: secp256r1 (prime256v1)
        """
        self.curve = curve
        self.backend = default_backend()
    
    def generate_keypair(self, name="user"):
        """
        Generate ECC keypair for user
        Returns: (private_key, public_key)
        """
        start_time = time.time()
        
        # Generate private key
        private_key = ec.generate_private_key(self.curve, self.backend)
        public_key = private_key.public_key()
        
        generation_time = time.time() - start_time
        
        # Save keys to PEM files
        self._save_private_key(private_key, f"{name}_private.pem")
        self._save_public_key(public_key, f"{name}_public.pem")
        
        return {
            'private_key': private_key,
            'public_key': public_key,
            'generation_time': generation_time,
            'private_key_file': f"{name}_private.pem",
            'public_key_file': f"{name}_public.pem"
        }
    
    def _save_private_key(self, private_key, filename):
        """Save private key to PEM file"""
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        
        with open(filename, 'wb') as f:
            f.write(pem)
    
    def _save_public_key(self, public_key, filename):
        """Save public key to PEM file"""
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        with open(filename, 'wb') as f:
            f.write(pem)
    
    def load_private_key(self, filename):
        """Load private key from PEM file"""
        with open(filename, 'rb') as f:
            pem_data = f.read()
        
        return serialization.load_pem_private_key(
            pem_data,
            password=None,
            backend=self.backend
        )
    
    def load_public_key(self, filename):
        """Load public key from PEM file"""
        with open(filename, 'rb') as f:
            pem_data = f.read()
        
        return serialization.load_pem_public_key(
            pem_data,
            backend=self.backend
        )
    
    def get_public_key_pem(self, public_key):
        """Get public key as PEM string"""
        pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        return pem.decode('utf-8')
