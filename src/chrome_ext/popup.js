const status = document.getElementById('status');

document.getElementById('startBtn').onclick = async () => {
  status.textContent = 'Starting...';
  try {
    const res = await fetch('http://localhost:8000/start-record', { method: 'POST' });
    status.textContent = res.ok ? 'Recording started.' : 'Failed to start.';
  } catch {
    status.textContent = 'Error connecting to server.';
  }
};

document.getElementById('stopBtn').onclick = async () => {
  status.textContent = 'Stopping...';
  try {
    const res = await fetch('http://localhost:8000/stop-record', { method: 'POST' });
    status.textContent = res.ok ? 'Recording stopped.' : 'Failed to stop.';
  } catch {
    status.textContent = 'Error connecting to server.';
  }
};

document.getElementById('translateBtn').onclick = async () => {
  status.textContent = 'Translating...';
  try {
    const res = await fetch('http://localhost:8000/translate-last', { method: 'GET' });
    if (res.ok) {
      const data = await res.json();
      status.textContent = data.text || 'Translated!';
    } else {
      status.textContent = 'Failed to translate.';
    }
  } catch {
    status.textContent = 'Error connecting to server.';
  }
};