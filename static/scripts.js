function sendMessage() {
    const userInput = document.getElementById('user-input').value;
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: userInput })
    })
    .then(response => response.json())
    .then(data => {
        const chatBox = document.getElementById('chat-box');
        chatBox.innerHTML += `<p><strong>You:</strong> ${userInput}</p>`;
        chatBox.innerHTML += `<p><strong>Bot:</strong> ${data.response}</p>`;
        document.getElementById('user-input').value = '';
    });
}