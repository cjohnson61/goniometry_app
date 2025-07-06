
document.addEventListener('DOMContentLoaded', function() {
    const captureBtn = document.getElementById('capture-btn');
    const messageArea = document.getElementById('message-area');
    const jointCheckboxesDiv = document.querySelector('.joint-checkboxes');

    // Function to fetch all joints and populate checkboxes
    function populateJointCheckboxes() {
        fetch('/get_all_joints')
            .then(response => response.json())
            .then(joints => {
                jointCheckboxesDiv.innerHTML = ''; // Clear existing checkboxes
                joints.forEach(joint => {
                    const checkboxContainer = document.createElement('div');
                    checkboxContainer.className = 'checkbox-container';

                    const checkbox = document.createElement('input');
                    checkbox.type = 'checkbox';
                    checkbox.id = joint;
                    checkbox.value = joint;
                    checkbox.checked = true; // All joints active by default
                    checkbox.addEventListener('change', sendActiveJoints);

                    const label = document.createElement('label');
                    label.htmlFor = joint;
                    label.textContent = formatJointName(joint);

                    checkboxContainer.appendChild(checkbox);
                    checkboxContainer.appendChild(label);
                    jointCheckboxesDiv.appendChild(checkboxContainer);
                });
            })
            .catch(error => console.error('Error fetching joints:', error));
    }

    // Function to send active joints to the backend
    function sendActiveJoints() {
        const activeJoints = Array.from(jointCheckboxesDiv.querySelectorAll('input[type="checkbox"]:checked'))
                                .map(checkbox => checkbox.value);
        
        fetch('/update_active_joints', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ active_joints: activeJoints }),
        })
        .then(response => response.json())
        .then(data => {
            if (data.status !== 'success') {
                console.error('Failed to update active joints:', data.message);
            }
        })
        .catch(error => console.error('Error sending active joints:', error));
    }

    // Helper function to format joint names for display
    function formatJointName(jointName) {
        return jointName.replace(/_/g, ' ').replace(/left|right/g, function(match) {
            return match.charAt(0).toUpperCase() + match.slice(1);
        }).replace(/flexion|abduction/g, function(match) {
            return match.charAt(0).toUpperCase() + match.slice(1);
        });
    }

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

    // Initial population of checkboxes
    populateJointCheckboxes();
});
