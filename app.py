"""
Hybrid ECC-AES192 Web Application
Flask backend for secure key exchange and file encryption
"""

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, flash
import os
import json
import time
from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge
import tempfile
import shutil

from crypto_modules import ECCManager, ECDHManager, AESManager

app = Flask(__name__)
app.secret_key = 'hybrid-ecc-aes192-secret-key-2023'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['KEYS_FOLDER'] = 'keys'
app.config['ENCRYPTED_FOLDER'] = 'encrypted'

# Create necessary directories
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['KEYS_FOLDER'], exist_ok=True)
os.makedirs(app.config['ENCRYPTED_FOLDER'], exist_ok=True)

# Initialize crypto managers
ecc_manager = ECCManager()
ecdh_manager = ECDHManager()
aes_manager = AESManager()

# Global variables to store session data (in production, use proper session management)
session_data = {
    'alice_keys': None,
    'bob_keys': None,
    'shared_secret_info': None,
    'performance_logs': []
}

@app.route('/')
def index():
    """Main page"""
    return render_template('index.html')

@app.route('/generate_keys')
def generate_keys():
    """Generate ECC keypairs for Alice and Bob"""
    try:
        # Clean up old keys before generating new ones
        cleanup_old_keys()
        
        # Generate Alice's keypair
        alice_keys = ecc_manager.generate_keypair('alice')
        
        # Generate Bob's keypair
        bob_keys = ecc_manager.generate_keypair('bob')
        
        # Store in session
        session_data['alice_keys'] = alice_keys
        session_data['bob_keys'] = bob_keys
        
        # Get PEM strings for display
        alice_public_pem = ecc_manager.get_public_key_pem(alice_keys['public_key'])
        bob_public_pem = ecc_manager.get_public_key_pem(bob_keys['public_key'])
        
        result = {
            'success': True,
            'alice_generation_time': alice_keys['generation_time'],
            'bob_generation_time': bob_keys['generation_time'],
            'total_generation_time': alice_keys['generation_time'] + bob_keys['generation_time'],
            'alice_public_key': alice_public_pem,
            'bob_public_key': bob_public_pem,
            'alice_private_file': alice_keys['private_key_file'],
            'alice_public_file': alice_keys['public_key_file'],
            'bob_private_file': bob_keys['private_key_file'],
            'bob_public_file': bob_keys['public_key_file']
        }
        
        # Log performance
        session_data['performance_logs'].append({
            'operation': 'Key Generation',
            'alice_time': alice_keys['generation_time'],
            'bob_time': bob_keys['generation_time'],
            'total_time': result['total_generation_time'],
            'timestamp': time.time()
        })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

def cleanup_old_keys():
    """Clean up old key files before generating new ones"""
    key_files = ['alice_private.pem', 'alice_public.pem', 'bob_private.pem', 'bob_public.pem']
    
    for key_file in key_files:
        if os.path.exists(key_file):
            try:
                os.remove(key_file)
            except Exception:
                pass  # Ignore errors during cleanup

@app.route('/key_exchange')
def key_exchange():
    """Perform ECDH key exchange"""
    try:
        if not session_data['alice_keys'] or not session_data['bob_keys']:
            return jsonify({'success': False, 'error': 'Keys not generated. Please generate keys first.'})
        
        # Perform key exchange verification
        verification = ecdh_manager.verify_key_exchange(
            session_data['alice_keys']['private_key'],
            session_data['alice_keys']['public_key'],
            session_data['bob_keys']['private_key'],
            session_data['bob_keys']['public_key']
        )
        
        session_data['shared_secret_info'] = verification
        
        result = {
            'success': True,
            'keys_match': verification['keys_match'],
            'shared_secrets_match': verification['shared_secrets_match'],
            'alice_aes_key': verification['alice_aes_key'],
            'alice_computation_time': verification['alice_computation_time'],
            'bob_computation_time': verification['bob_computation_time'],
            'alice_derivation_time': verification['alice_derivation_time'],
            'bob_derivation_time': verification['bob_derivation_time'],
            'total_alice_time': verification['total_alice_time'],
            'total_bob_time': verification['total_bob_time'],
            'verification_time': verification['verification_time']
        }
        
        # Log performance
        session_data['performance_logs'].append({
            'operation': 'Key Exchange (ECDH + HKDF)',
            'alice_time': verification['total_alice_time'],
            'bob_time': verification['total_bob_time'],
            'total_time': verification['total_alice_time'] + verification['total_bob_time'],
            'timestamp': time.time()
        })
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/encrypt_file', methods=['POST'])
def encrypt_file():
    """Encrypt uploaded file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if not session_data['shared_secret_info']:
            return jsonify({'success': False, 'error': 'Key exchange not performed. Please perform key exchange first.'})
        
        # Get encryption mode
        mode = request.form.get('mode', 'gcm')
        
        # Save uploaded file
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Get AES key from session
        alice_keys = session_data['alice_keys']
        bob_public_key = session_data['bob_keys']['public_key']
        
        # Compute shared secret and derive AES key
        shared_secret = ecdh_manager.compute_shared_secret(
            alice_keys['private_key'], 
            bob_public_key
        )
        aes_key_info = ecdh_manager.derive_aes_key(shared_secret['shared_secret'])
        aes_key = aes_key_info['aes_key']
        
        # Encrypt file
        if mode == 'gcm':
            encryption_result = aes_manager.encrypt_file_gcm(file_path, aes_key)
        else:
            encryption_result = aes_manager.encrypt_file_cbc(file_path, aes_key)
        
        # Move encrypted file to encrypted folder
        encrypted_filename = os.path.basename(encryption_result['encrypted_file_path'])
        encrypted_final_path = os.path.join(app.config['ENCRYPTED_FOLDER'], encrypted_filename)
        shutil.move(encryption_result['encrypted_file_path'], encrypted_final_path)
        
        result = {
            'success': True,
            'original_filename': filename,
            'encrypted_filename': encrypted_filename,
            'encryption_time': encryption_result['encryption_time'],
            'original_size': encryption_result['original_size'],
            'encrypted_size': encryption_result['encrypted_size'],
            'size_increase': encryption_result['size_increase'],
            'size_increase_percent': encryption_result['size_increase_percent'],
            'algorithm': 'AES-192-GCM' if mode == 'gcm' else 'AES-192-CBC'
        }
        
        if mode == 'gcm':
            result['nonce'] = encryption_result['nonce']
            result['tag'] = encryption_result['tag']
        else:
            result['iv'] = encryption_result['iv']
        
        # Log performance
        session_data['performance_logs'].append({
            'operation': f'File Encryption ({result["algorithm"]})',
            'encryption_time': encryption_result['encryption_time'],
            'original_size': encryption_result['original_size'],
            'encrypted_size': encryption_result['encrypted_size'],
            'timestamp': time.time()
        })
        
        # Clean up original file
        os.remove(file_path)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/decrypt_file', methods=['POST'])
def decrypt_file():
    """Decrypt uploaded encrypted file"""
    try:
        if 'file' not in request.files:
            return jsonify({'success': False, 'error': 'No file uploaded'})
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'success': False, 'error': 'No file selected'})
        
        if not session_data['shared_secret_info']:
            return jsonify({'success': False, 'error': 'Key exchange not performed. Please perform key exchange first.'})
        
        # Save uploaded encrypted file
        filename = secure_filename(file.filename)
        encrypted_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(encrypted_file_path)
        
        # Get AES key from session (Bob's perspective)
        bob_keys = session_data['bob_keys']
        alice_public_key = session_data['alice_keys']['public_key']
        
        # Compute shared secret and derive AES key
        shared_secret = ecdh_manager.compute_shared_secret(
            bob_keys['private_key'], 
            alice_public_key
        )
        aes_key_info = ecdh_manager.derive_aes_key(shared_secret['shared_secret'])
        aes_key = aes_key_info['aes_key']
        
        # Determine encryption mode by checking file content
        with open(encrypted_file_path, 'r') as f:
            encrypted_package = json.load(f)
        
        if encrypted_package.get('algorithm') == 'AES-192-GCM':
            decryption_result = aes_manager.decrypt_file_gcm(encrypted_file_path, aes_key)
        else:
            decryption_result = aes_manager.decrypt_file_cbc(encrypted_file_path, aes_key)
        
        if not decryption_result['success']:
            return jsonify({'success': False, 'error': decryption_result['error']})
        
        # Move decrypted file to uploads folder
        decrypted_filename = os.path.basename(decryption_result['decrypted_file_path'])
        decrypted_final_path = os.path.join(app.config['UPLOAD_FOLDER'], decrypted_filename)
        shutil.move(decryption_result['decrypted_file_path'], decrypted_final_path)
        
        result = {
            'success': True,
            'original_encrypted_filename': filename,
            'decrypted_filename': decrypted_filename,
            'decryption_time': decryption_result['decryption_time'],
            'original_encrypted_size': decryption_result['original_encrypted_size'],
            'decrypted_size': decryption_result['decrypted_size']
        }
        
        # Log performance
        session_data['performance_logs'].append({
            'operation': 'File Decryption',
            'decryption_time': decryption_result['decryption_time'],
            'original_encrypted_size': decryption_result['original_encrypted_size'],
            'decrypted_size': decryption_result['decrypted_size'],
            'timestamp': time.time()
        })
        
        # Clean up encrypted file
        os.remove(encrypted_file_path)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/download_file/<filename>')
def download_file(filename):
    """Download file from uploads or encrypted folder"""
    try:
        # Try uploads folder first
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        
        # Try encrypted folder
        file_path = os.path.join(app.config['ENCRYPTED_FOLDER'], filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        
        return jsonify({'success': False, 'error': 'File not found'})
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/performance')
def performance():
    """Get performance analysis"""
    try:
        logs = session_data['performance_logs']
        
        # Calculate statistics
        total_operations = len(logs)
        if total_operations == 0:
            return jsonify({'success': True, 'logs': [], 'statistics': {}})
        
        # Group by operation type
        key_gen_logs = [log for log in logs if 'Key Generation' in log['operation']]
        key_exchange_logs = [log for log in logs if 'Key Exchange' in log['operation']]
        encryption_logs = [log for log in logs if 'Encryption' in log['operation']]
        decryption_logs = [log for log in logs if 'Decryption' in log['operation']]
        
        statistics = {
            'total_operations': total_operations,
            'key_generation_count': len(key_gen_logs),
            'key_exchange_count': len(key_exchange_logs),
            'encryption_count': len(encryption_logs),
            'decryption_count': len(decryption_logs),
            'average_key_generation_time': sum(log['total_time'] for log in key_gen_logs) / len(key_gen_logs) if key_gen_logs else 0,
            'average_key_exchange_time': sum(log['total_time'] for log in key_exchange_logs) / len(key_exchange_logs) if key_exchange_logs else 0,
            'average_encryption_time': sum(log['encryption_time'] for log in encryption_logs) / len(encryption_logs) if encryption_logs else 0,
            'average_decryption_time': sum(log['decryption_time'] for log in decryption_logs) / len(decryption_logs) if decryption_logs else 0,
        }
        
        return jsonify({
            'success': True,
            'logs': logs,
            'statistics': statistics
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/reset')
def reset():
    """Reset session data"""
    global session_data
    session_data = {
        'alice_keys': None,
        'bob_keys': None,
        'shared_secret_info': None,
        'performance_logs': []
    }
    
    # Clean up files
    for folder in [app.config['UPLOAD_FOLDER'], app.config['KEYS_FOLDER'], app.config['ENCRYPTED_FOLDER']]:
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path):
                    os.unlink(file_path)
            except Exception:
                pass
    
    return jsonify({'success': True, 'message': 'System reset successfully'})

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'success': False, 'error': 'File too large. Maximum size is 16MB.'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5002)
