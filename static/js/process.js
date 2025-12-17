// Process tab specific JavaScript
let currentStep = 1;
let processState = {
  keysGenerated: false,
  keyExchanged: false,
};

function updateStepper() {
  document.querySelectorAll('.process-step').forEach((step, index) => {
    if (index + 1 <= currentStep) {
      step.classList.add('active');
    } else {
      step.classList.remove('active');
    }
  });
}

function showStep(stepNumber) {
  document.querySelectorAll('.step-content').forEach((content) => {
    content.classList.remove('active');
  });
  document.getElementById(`step${stepNumber}`).classList.add('active');
  currentStep = stepNumber;
  updateStepper();
}

function updateFileInfo(input, type) {
  const file = input.files[0];
  const infoElement = document.getElementById(`${type}FileInfo`);
  if (file) {
    infoElement.textContent = `Selected: ${file.name} (${(
      file.size / 1024
    ).toFixed(2)} KB)`;
  } else {
    infoElement.textContent = '';
  }
}

// Helper: format bytes to human-readable string
function formatBytes(bytes, decimals = 2) {
  if (!bytes && bytes !== 0) return '-';
  if (bytes === 0) return '0 B';
  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(dm)) + ' ' + sizes[i];
}

// Override existing functions to work with new UI
async function generateKeys() {
  const btn = document.getElementById('generateKeysBtn');
  btn.disabled = true;
  btn.textContent = 'Generating...';

  try {
    const response = await fetch('/generate_keys');
    const result = await response.json();

    if (result.success) {
      processState.keysGenerated = true;

      const resultsDiv = document.getElementById('keyResults');
      resultsDiv.innerHTML = `
                <div class="process-success">✓ Kunci Publik Alice dibuat</div>
                <div class="process-success">✓ Kunci Publik Bob dibuat</div>
                <div style="margin-top: 12px; font-size: 12px; color: var(--muted);">
                    Waktu: ${result.total_generation_time.toFixed(4)}s
                </div>
            `;

      // Update key display in step 2 (show full PEM in textarea)
      document.getElementById('alicePubKey').value = result.alice_public_key;
      document.getElementById('bobPubKey').value = result.bob_public_key;

      // Enable key exchange button
      document.getElementById('keyExchangeBtn').disabled = false;

      // Auto-advance to step 2 after a short delay
      setTimeout(() => {
        showStep(2);
      }, 1500);
    } else {
      document.getElementById('keyResults').innerHTML = `
                <div style="color: var(--danger);">Error: ${result.error}</div>
            `;
    }
  } catch (error) {
    document.getElementById('keyResults').innerHTML = `
            <div style="color: var(--danger);">Network error: ${error.message}</div>
        `;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Buat Keypair';
  }
}

async function performKeyExchange() {
  const btn = document.getElementById('keyExchangeBtn');
  btn.disabled = true;
  btn.textContent = 'Bertukar...';

  try {
    const response = await fetch('/key_exchange');
    const result = await response.json();

    if (result.success) {
      processState.keyExchanged = true;

      const resultsDiv = document.getElementById('exchangeResults');
      resultsDiv.innerHTML = `
                <div class="process-success">✓ Pertukaran kunci berhasil</div>
                <div class="process-success">✓ Kunci AES-192 berhasil diturunkan</div>
                <div style="margin-top: 12px; font-size: 12px; color: var(--muted);">
                    Kunci cocok: ${result.keys_match ? 'Ya' : 'Tidak'}<br>
                    Shared secrets cocok: ${
                      result.shared_secrets_match ? 'Ya' : 'Tidak'
                    }<br>
                    Waktu: ${(
                      result.total_alice_time + result.total_bob_time
                    ).toFixed(4)}s
                </div>
            `;

      // Enable encrypt/decrypt buttons
      document.getElementById('encryptBtn').disabled = false;
      document.getElementById('decryptBtn').disabled = false;

      // Auto-advance to step 3 after a short delay
      setTimeout(() => {
        showStep(3);
      }, 1500);
    } else {
      document.getElementById('exchangeResults').innerHTML = `
                <div style="color: var(--danger);">Error: ${result.error}</div>
            `;
    }
  } catch (error) {
    document.getElementById('exchangeResults').innerHTML = `
            <div style="color: var(--danger);">Network error: ${error.message}</div>
        `;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Lakukan Pertukaran Kunci';
  }
}

// Copy public key to clipboard
function copyToClipboard(elementId) {
  const el = document.getElementById(elementId);
  if (!el) return;
  const value = el.value || el.textContent || '';
  navigator.clipboard
    .writeText(value)
    .then(() => {
      alert('Kunci disalin ke clipboard');
    })
    .catch(() => {
      alert('Gagal menyalin kunci');
    });
}

async function encryptFile() {
  const fileInput = document.getElementById('encryptFile');
  const file = fileInput.files[0];

  if (!file) {
    alert('Silakan pilih file untuk dienkripsi');
    return;
  }

  const btn = document.getElementById('encryptBtn');
  btn.disabled = true;
  btn.textContent = 'Sedang mengenkripsi...';

  try {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('mode', document.getElementById('encryptMode').value);

    const response = await fetch('/encrypt_file', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();

    if (result.success) {
      const resultsDiv = document.getElementById('encryptResults');
      resultsDiv.innerHTML = `
                <div class="process-success">✓ File berhasil dienkripsi</div>
                <div style="margin-top: 12px; font-size: 12px; color: var(--muted);">
                    Original: ${result.original_filename} (${formatBytes(
        result.original_size
      )})<br>
                    Terenkripsi: ${result.encrypted_filename} (${formatBytes(
        result.encrypted_size
      )})<br>
                    Algoritma: ${result.algorithm}<br>
                    Ukuran File: ${formatBytes(result.size_increase)}<br>
                    Waktu: ${result.encryption_time.toFixed(4)}s
                </div>
                <button class="process-button" style="margin-top: 12px; padding: 6px 12px; font-size: 12px;" 
                        onclick="window.open('/download_file/${
                          result.encrypted_filename
                        }', '_blank')">
                    Unduh File Terenkripsi
                </button>
            `;

      // Auto-advance to step 4 after a short delay
      setTimeout(() => {
        showStep(4);
      }, 1500);
    } else {
      document.getElementById('encryptResults').innerHTML = `
                <div style="color: var(--danger);">Error: ${result.error}</div>
            `;
    }
  } catch (error) {
    document.getElementById('encryptResults').innerHTML = `
            <div style="color: var(--danger);">Network error: ${error.message}</div>
        `;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Enkripsi File';
  }
}

async function decryptFile() {
  const fileInput = document.getElementById('decryptFile');
  const file = fileInput.files[0];

  if (!file) {
    alert('Silakan pilih file untuk didekripsi');
    return;
  }

  const btn = document.getElementById('decryptBtn');
  btn.disabled = true;
  btn.textContent = 'Sedang mendekripsi...';

  try {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch('/decrypt_file', {
      method: 'POST',
      body: formData,
    });

    const result = await response.json();

    if (result.success) {
      const resultsDiv = document.getElementById('decryptResults');
      resultsDiv.innerHTML = `
                <div class="process-success">✓ File berhasil didekripsi</div>
                <div style="margin-top: 12px; font-size: 12px; color: var(--muted);">
                    Terenkripsi: ${
                      result.original_encrypted_filename
                    } (${formatBytes(result.original_encrypted_size)})<br>
                    Didekripsi: ${result.decrypted_filename} (${formatBytes(
        result.decrypted_size
      )})<br>
                    Waktu: ${result.decryption_time.toFixed(4)}s
                </div>
                <button class="process-button" style="margin-top: 12px; padding: 6px 12px; font-size: 12px;" 
                        onclick="window.open('/download_file/${
                          result.decrypted_filename
                        }', '_blank')">
                    Unduh File Didekripsi
                </button>
            `;
    } else {
      document.getElementById('decryptResults').innerHTML = `
                <div style="color: var(--danger);">Error: ${result.error}</div>
            `;
    }
  } catch (error) {
    document.getElementById('decryptResults').innerHTML = `
            <div style="color: var(--danger);">Network error: ${error.message}</div>
        `;
  } finally {
    btn.disabled = false;
    btn.textContent = 'Dekripsi File';
  }
}

// Override reset system function
async function resetSystem() {
  if (
    !confirm(
      'Are you sure you want to reset the system? All keys and files will be deleted.'
    )
  ) {
    return;
  }

  try {
    const response = await fetch('/reset');
    const result = await response.json();

    if (result.success) {
      processState = {
        keysGenerated: false,
        keyExchanged: false,
      };

      // Clear all results
      document.getElementById('keyResults').innerHTML = '';
      document.getElementById('exchangeResults').innerHTML = '';
      document.getElementById('encryptResults').innerHTML = '';
      document.getElementById('decryptResults').innerHTML = '';

      // Reset key display (textarea)
      document.getElementById('alicePubKey').value = 'Belum dibuat';
      document.getElementById('bobPubKey').value = 'Belum dibuat';

      // Disable buttons
      document.getElementById('keyExchangeBtn').disabled = true;
      document.getElementById('encryptBtn').disabled = true;
      document.getElementById('decryptBtn').disabled = true;

      // Clear file inputs
      document.getElementById('encryptFile').value = '';
      document.getElementById('decryptFile').value = '';
      document.getElementById('encryptFileInfo').textContent = '';
      document.getElementById('decryptFileInfo').textContent = '';

      // Reset to step 1
      showStep(1);

      alert('System reset successfully!');
    } else {
      alert('Error resetting system: ' + result.error);
    }
  } catch (error) {
    alert('Network error: ' + error.message);
  }
}

// Add click handlers for stepper navigation
document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.process-step').forEach((step) => {
    step.addEventListener('click', function () {
      const stepNumber = parseInt(this.dataset.step);

      // Only allow navigation to completed steps or current step
      if (
        stepNumber <= currentStep ||
        (stepNumber === 2 && processState.keysGenerated) ||
        (stepNumber === 3 && processState.keyExchanged) ||
        (stepNumber === 4 && processState.keyExchanged)
      ) {
        showStep(stepNumber);
      }
    });
  });
});
