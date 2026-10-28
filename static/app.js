const chatArea = document.getElementById('chatArea');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const micBtn = document.getElementById('micBtn');

function appendMessage(role, text) {
  const wrapper = document.createElement('div');
  wrapper.className = `message ${role}`;

  const bubble = document.createElement('div');
  bubble.className = 'bubble';
  bubble.textContent = text;

  wrapper.appendChild(bubble);
  chatArea.appendChild(wrapper);
  chatArea.scrollTop = chatArea.scrollHeight;
}

async function sendMessage() {
  const text = messageInput.value.trim();
  if (!text) return;

  appendMessage('user', text);
  messageInput.value = '';

  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text }),
    });

    const data = await response.json();
    const reply = data.reply || 'I’m here to help.';
    appendMessage('assistant', reply);

    if ('speechSynthesis' in window) {
      const utterance = new SpeechSynthesisUtterance(reply);
      utterance.rate = 1;
      utterance.pitch = 1.1;
      window.speechSynthesis.cancel();
      window.speechSynthesis.speak(utterance);
    }
  } catch (error) {
    appendMessage('assistant', 'I hit an error while responding. Please try again.');
  }
}

sendBtn.addEventListener('click', sendMessage);
messageInput.addEventListener('keydown', (event) => {
  if (event.key === 'Enter') {
    sendMessage();
  }
});

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  const recognition = new SpeechRecognition();
  recognition.lang = 'en-US';
  recognition.interimResults = false;

  micBtn.addEventListener('click', () => {
    recognition.start();
  });

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    messageInput.value = transcript;
    sendMessage();
  };
} else {
  micBtn.title = 'Voice input is not supported in this browser';
}
