(function() {
    // 1. إعدادات البوت
    const API_URL = "https://smart-website-assistant.onrender.com";
    
    // 2. إنشاء حاوية الـ Widget (Shadow DOM)
    const host = document.createElement('div');
    host.id = 'smart-chatbot-host';
    document.body.appendChild(host);
    const shadow = host.attachShadow({ mode: 'open' });

    // 3. حقن الـ CSS
    const style = document.createElement('style');
    style.textContent = `
        .chat-btn { position: fixed; bottom: 20px; right: 20px; width: 60px; height: 60px; border-radius: 50%; background: #007bff; color: white; border: none; cursor: pointer; box-shadow: 0 4px 12px rgba(0,0,0,0.2); font-size: 24px; z-index: 9999; }
        .chat-window { position: fixed; bottom: 90px; right: 20px; width: 350px; height: 500px; background: white; border-radius: 12px; box-shadow: 0 5px 20px rgba(0,0,0,0.15); display: none; flex-direction: column; z-index: 9999; overflow: hidden; font-family: sans-serif; }
        .chat-header { background: #007bff; color: white; padding: 15px; display: flex; justify-content: space-between; align-items: center; }
        .chat-messages { flex: 1; padding: 15px; overflow-y: auto; background: #f9f9f9; display: flex; flex-direction: column; gap: 10px; }
        .msg { max-width: 80%; padding: 10px; border-radius: 8px; font-size: 14px; }
        .msg.user { background: #007bff; color: white; align-self: flex-end; border-bottom-right-radius: 0; }
        .msg.bot { background: #e9ecef; color: #333; align-self: flex-start; border-bottom-left-radius: 0; }
        .chat-input { display: flex; padding: 10px; background: white; border-top: 1px solid #ddd; }
        .chat-input input { flex: 1; border: 1px solid #ccc; padding: 8px; border-radius: 20px; outline: none; }
        .chat-input button { background: #007bff; color: white; border: none; border-radius: 50%; width: 36px; height: 36px; margin-left: 8px; cursor: pointer; }
        .suggestions { display: flex; flex-wrap: wrap; gap: 5px; padding: 10px; background: white; }
        .suggestion-btn { background: #f1f3f5; border: 1px solid #dee2e6; padding: 5px 10px; border-radius: 15px; font-size: 12px; cursor: pointer; }
    `;
    shadow.appendChild(style);

    // 4. بناء الواجهة
    const btn = document.createElement('button');
    btn.className = 'chat-btn';
    btn.innerHTML = '💬';

    const win = document.createElement('div');
    win.className = 'chat-window';
    win.innerHTML = `
        <div class="chat-header">
            <span>المساعد الذكي</span>
            <button style="background:none;border:none;color:white;cursor:pointer;" id="closeBtn">✖</button>
        </div>
        <div class="chat-messages" id="messages"></div>
        <div class="suggestions" id="suggestions"></div>
        <div class="chat-input">
            <input type="text" id="inputField" placeholder="اكتب رسالتك...">
            <button id="sendBtn">➤</button>
        </div>
    `;
    shadow.appendChild(btn);
    shadow.appendChild(win);

    // 5. المنطق (JavaScript)
    const messagesArea = shadow.getElementById('messages');
    const inputField = shadow.getElementById('inputField');
    const sendBtn = shadow.getElementById('sendBtn');
    const suggestionsArea = shadow.getElementById('suggestions');
    const closeBtn = shadow.getElementById('closeBtn');

    btn.onclick = () => win.style.display = 'flex';
    closeBtn.onclick = () => win.style.display = 'none';

    function addMessage(text, sender) {
        const div = document.createElement('div');
        div.className = `msg ${sender}`;
        div.textContent = text;
        messagesArea.appendChild(div);
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    async function sendMessage(text, source = "text") {
        if (!text.trim()) return;
        addMessage(text, 'user');
        inputField.value = '';
        suggestionsArea.innerHTML = '';

        try {
            const res = await fetch(`${API_URL}/api/chat`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: text, language: "ar", source: source })
            });
            const data = await res.json();
            addMessage(data.reply, 'bot');
            
            // إضافة الأزرار الجاهزة
            if (data.suggestions && data.suggestions.length > 0) {
                data.suggestions.forEach(s => {
                    const b = document.createElement('button');
                    b.className = 'suggestion-btn';
                    b.textContent = s.text;
                    b.onclick = () => sendMessage(s.text, 'quick_reply');
                    suggestionsArea.appendChild(b);
                });
            }
        } catch (e) {
            addMessage("عذراً، حدث خطأ في الاتصال.", 'bot');
        }
    }

    sendBtn.onclick = () => sendMessage(inputField.value);
    inputField.onkeypress = (e) => { if (e.key === 'Enter') sendMessage(inputField.value); };

    // رسالة الترحيب
    setTimeout(() => addMessage("مرحباً بك! كيف يمكنني مساعدتك اليوم؟", 'bot'), 500);
})();
