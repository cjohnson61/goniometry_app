
document.addEventListener('DOMContentLoaded', function() {
    const captureBtn = document.getElementById('capture-btn');
    const messageArea = document.getElementById('message-area');

    if (captureBtn) {
        captureBtn.addEventListener('click', function() {
            fetch('/capture_measurement', {
                method: 'POST',
            })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    messageArea.textContent = 'Measurement captured and saved!';
                    messageArea.style.color = 'green';
                } else {
                    messageArea.textContent = 'Error: ' + data.message;
                    messageArea.style.color = 'red';
                }
            })
            .catch(error => {
                console.error('Error:', error);
                messageArea.textContent = 'An error occurred while capturing measurement.';
                messageArea.style.color = 'red';
            });
        });
    }
});
