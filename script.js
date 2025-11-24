let chatMessages = document.getElementById('chatMessages');
let userInput = document.getElementById('userInput');
let chartContainer = document.getElementById('chartContainer');
let alertsContainer = document.getElementById('alertsContainer');

// Handle Enter key press
userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

function sendMessage() {
    const message = userInput.value.trim();
    if (message === '') return;
    
    // Add user message to chat
    addMessage(message, 'user');
    userInput.value = '';
    
    // Send to backend
    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => response.json())
    .then(data => {
        // Add bot response
        addMessage(data.response, 'bot');
        
        // Display chart if available
        if (data.chart) {
            chartContainer.innerHTML = `<img src="${data.chart}" alt="Production Chart">`;
        } else {
            chartContainer.innerHTML = '';
        }
        
        // Display alerts if any
        displayAlerts(data.alerts);
    })
    .catch(error => {
        console.error('Error:', error);
        addMessage('Sorry, there was an error processing your request.', 'bot');
    });
}

function addMessage(content, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;
    
    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';
    contentDiv.textContent = content;
    
    messageDiv.appendChild(contentDiv);
    chatMessages.appendChild(messageDiv);
    
    // Scroll to bottom
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function quickAction(action) {
    userInput.value = action;
    sendMessage();
}

function displayAlerts(alerts) {
    alertsContainer.innerHTML = '';
    
    if (alerts && alerts.length > 0) {
        alerts.forEach(alert => {
            const alertDiv = document.createElement('div');
            alertDiv.className = 'alert';
            alertDiv.textContent = alert;
            alertsContainer.appendChild(alertDiv);
        });
    }
}

// Initial alerts check on page load
document.addEventListener('DOMContentLoaded', function() {
    fetch('/chatbot', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: 'check alerts' })
    })
    .then(response => response.json())
    .then(data => {
        displayAlerts(data.alerts);
    });
});