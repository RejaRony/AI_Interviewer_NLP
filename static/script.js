// script.js (V3 - Definitive Live Connection)

document.addEventListener('DOMContentLoaded', () => {
    // These IDs now perfectly match the new index.html
    const messageForm = document.getElementById('message-form');
    const messageInput = document.getElementById('messageInput');
    const sendButton = document.getElementById('sendButton');
    const messageArea = document.getElementById('messageArea');

    const sendMessage = async (event) => {
        event.preventDefault(); // Prevent the form from reloading the page
        const messageText = messageInput.value.trim();
        if (messageText === '') return;

        // --- NEW LOGIC ADDED HERE: Remove Jinja-rendered initial message ---
        const initialMessageJinja = messageArea.querySelector('.initial-message-jinja');
        if (initialMessageJinja) {
            initialMessageJinja.remove(); 
        }

        displayMessage(messageText, 'user');
        messageInput.value = '';

        // Disable the form while the AI is "thinking"
        sendButton.disabled = true;
        messageInput.disabled = true;

        try {
            // This is the live wire to our Python backend
            const response = await fetch('/get_response', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: messageText }),
            });

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            const data = await response.json();
            displayMessage(data.response, 'ai');

        } catch (error) {
            console.error('Error fetching AI response:', error);
            displayMessage('Sorry, I seem to be having trouble connecting to my brain right now.', 'ai');
        } finally {
            // Re-enable the form after the response is received
            sendButton.disabled = false;
            messageInput.disabled = false;
            messageInput.focus();
        }
    };

    const displayMessage = (message, sender) => {
        const messageElement = document.createElement('div');
        // Your CSS uses .user and .other, so we will use .other for the AI
        const senderClass = sender === 'user' ? 'user' : 'other';
        messageElement.classList.add('message', senderClass);
        messageElement.innerHTML = message;
        messageArea.appendChild(messageElement);
        messageArea.scrollTop = messageArea.scrollHeight;
    };

    messageForm.addEventListener('submit', sendMessage);
});