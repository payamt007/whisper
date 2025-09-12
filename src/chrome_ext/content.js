chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    if (request.action === 'insertText') {
        const textarea = document.getElementById('copilot-chat-textarea');
        if (textarea) {
            textarea.value = request.text;
        }
    }
});
