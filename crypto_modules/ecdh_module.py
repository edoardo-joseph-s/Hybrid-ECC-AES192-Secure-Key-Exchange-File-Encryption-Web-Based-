"""
ECDH Module for Hybrid ECC-AES192 System
Handles Elliptic Curve Diffie-Hellman key exchange
"""

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
import time

class ECDHManager:
    def __init__(self):
        """Initialize ECDH Manager"""
        self.backend = default_backend()
    
    def compute_shared_secret(self, private_key, peer_public_key):
        """
        Compute shared secret using ECDH
        Args:
            private_key: Your private key
            peer_public_key: Peer's public key
        Returns:
            dict with shared_secret and computation_time
        """
        start_time = time.time()
        
        # Perform ECDH key exchange
        shared_secret = private_key.exchange(ec.ECDH(), peer_public_key)
        
        computation_time = time.time() - start_time
        
        return {
            'shared_secret': shared_secret,
            'computation_time': computation_time,
            'secret_length': len(shared_secret) * 8  # in bits
        }
    
    def derive_aes_key(self, shared_secret, salt=None, info=b"AES-192-Key"):
        """
        Derive AES-192 key from shared secret using HKDF
        Args:
            shared_secret: ECDH shared secret
            salt: Optional salt (None for random salt)
            info: Context info for HKDF
        Returns:
            dict with aes_key and derivation_time
        """
        start_time = time.time()
        
        # If no salt provided, use bytes of length equal to hash output
        if salt is None:
            salt = b'\x00' * 32  # Zero salt for consistency
        
        # Derive key using HKDF with SHA-256
        hkdf = HKDF(
            algorithm=hashes.SHA256(),
            length=24,  # 192 bits = 24 bytes for AES-192
            salt=salt,
            info=info,
            backend=self.backend
        )
        
        aes_key = hkdf.derive(shared_secret)
        
        derivation_time = time.time() - start_time
        
        return {
            'aes_key': aes_key,
            'derivation_time': derivation_time,
            'key_length': len(aes_key) * 8,  # in bits
            'salt': salt,
            'info': info
        }
    
    def verify_key_exchange(self, alice_private, alice_public, bob_private, bob_public):
        """
        Verify that both parties derive the same AES key
        Args:
            alice_private, alice_public: Alice's key pair
            bob_private, bob_public: Bob's key pair
        Returns:
            dict with verification results
        """
        start_time = time.time()
        
        # Alice computes shared secret with Bob's public key
        alice_shared = self.compute_shared_secret(alice_private, bob_public)
        alice_aes = self.derive_aes_key(alice_shared['shared_secret'])
        
        # Bob computes shared secret with Alice's public key
        bob_shared = self.compute_shared_secret(bob_private, alice_public)
        bob_aes = self.derive_aes_key(bob_shared['shared_secret'])
        
        verification_time = time.time() - start_time
        
        # Verify both derived keys are identical
        keys_match = alice_aes['aes_key'] == bob_aes['aes_key']
        shared_secrets_match = alice_shared['shared_secret'] == bob_shared['shared_secret']
        
        return {
            'keys_match': keys_match,
            'shared_secrets_match': shared_secrets_match,
            'alice_aes_key': alice_aes['aes_key'].hex() if keys_match else None,
            'bob_aes_key': bob_aes['aes_key'].hex() if keys_match else None,
            'alice_computation_time': alice_shared['computation_time'],
            'bob_computation_time': bob_shared['computation_time'],
            'alice_derivation_time': alice_aes['derivation_time'],
            'bob_derivation_time': bob_aes['derivation_time'],
            'verification_time': verification_time,
            'total_alice_time': alice_shared['computation_time'] + alice_aes['derivation_time'],
            'total_bob_time': bob_shared['computation_time'] + bob_aes['derivation_time']
        }
