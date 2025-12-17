// Global state
let systemState = {
  keysGenerated: false,
  keyExchanged: false,
};

// Show loading spinner
function showLoading(buttonId) {
  $(`#${buttonId}`).prop('disabled', true);
  $(`#${buttonId} .loading`).addClass('show');
}

// Hide loading spinner
function hideLoading(buttonId) {
  $(`#${buttonId}`).prop('disabled', false);
  $(`#${buttonId} .loading`).removeClass('show');
}

// Load Performance Data
async function loadPerformance() {
  try {
    const response = await fetch('/performance');
    const result = await response.json();

    if (result.success) {
      displayPerformanceStats(result.statistics);
      displayPerformanceLogs(result.logs);
    } else {
      showAlert('Error loading performance data: ' + result.error, 'error');
    }
  } catch (error) {
    showAlert('Network error: ' + error.message, 'error');
  }
}

// Display Performance Statistics
function displayPerformanceStats(stats) {
  const statsHtml = `
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title text-primary">${stats.total_operations}</h5>
                    <p class="card-text">Total Operations</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title text-success">${stats.key_generation_count}</h5>
                    <p class="card-text">Key Generations</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title text-info">${stats.encryption_count}</h5>
                    <p class="card-text">Enkripsi</p>
                </div>
            </div>
        </div>
        <div class="col-md-3">
            <div class="card text-center">
                <div class="card-body">
                    <h5 class="card-title text-warning">${stats.decryption_count}</h5>
                    <p class="card-text">Dekripsi</p>
                </div>
            </div>
        </div>
    `;
  $('#statsCards').html(statsHtml);
}

// Display Performance Logs
function displayPerformanceLogs(logs) {
  let logsHtml = '';
  logs.forEach((log) => {
    const timestamp = new Date(log.timestamp * 1000).toLocaleString();
    let details = '';

    if (log.operation.includes('Key Generation')) {
      details = `Total: ${log.total_time.toFixed(6)}s`;
    } else if (log.operation.includes('Key Exchange')) {
      details = `Alice: ${log.alice_time.toFixed(
        6
      )}s, Bob: ${log.bob_time.toFixed(6)}s`;
    } else if (log.operation.includes('Encryption')) {
      details = `Waktu: ${log.encryption_time.toFixed(6)}s, Ukuran: ${
        log.original_size
      } bytes`;
    } else if (log.operation.includes('Decryption')) {
      details = `Waktu: ${log.decryption_time.toFixed(6)}s, Ukuran: ${
        log.decrypted_size
      } bytes`;
    }

    logsHtml += `
            <tr>
                <td>${log.operation}</td>
                <td>${
                  details.includes('Time:')
                    ? details.match(/Time: [\d.]+s/)[0]
                    : details
                }</td>
                <td>${details}</td>
                <td>${timestamp}</td>
            </tr>
        `;
  });

  $('#logsTable tbody').html(
    logsHtml ||
      '<tr><td colspan="4" class="text-center">No logs available</td></tr>'
  );
}

// Show Alert
function showAlert(message, type) {
  const alertClass = type === 'error' ? 'alert-danger' : 'alert-success';
  const alertHtml = `
        <div class="alert ${alertClass} alert-dismissible fade show position-fixed" style="top: 20px; right: 20px; z-index: 1050;">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        </div>
    `;
  $('body').append(alertHtml);

  // Auto dismiss after 5 seconds
  setTimeout(() => {
    $('.alert').alert('close');
  }, 5000);
}

// Initialize on page load
$(document).ready(function () {
  // Load performance data when analysis tab is shown
  $('button[data-bs-target="#analysis"]').on('shown.bs.tab', function () {
    loadPerformance();
  });
});
