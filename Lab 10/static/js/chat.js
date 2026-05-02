
let loading = false;

const messagesDiv = document.getElementById("messages");
const inputBox    = document.getElementById("userInput");
const sendButton  = document.getElementById("sendBtn");


function addMessage(role, text) {
  const row    = document.createElement("div");
  row.className = "msg " + role;        

  const bubble = document.createElement("div");
  bubble.className = "bubble";
  bubble.textContent = text;              

  row.appendChild(bubble);
  messagesDiv.appendChild(row);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;   
}


function showTyping() {
  const row    = document.createElement("div");
  row.className = "msg bot";
  row.id        = "typing";

  const bubble  = document.createElement("div");
  bubble.className = "bubble";
  bubble.innerHTML = `<div class="typing">
    <div class="dot"></div>
    <div class="dot"></div>
    <div class="dot"></div>
  </div>`;

  row.appendChild(bubble);
  messagesDiv.appendChild(row);
  messagesDiv.scrollTop = messagesDiv.scrollHeight;
}


function hideTyping() {
  const t = document.getElementById("typing");
  if (t) t.remove();
}


async function sendMessage() {
  if (loading) return;

  const text = inputBox.value.trim();
  if (!text) return;

  inputBox.value = "";
  addMessage("user", text);


  loading = true;
  sendButton.disabled = true;
  showTyping();

  try {

    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: text })
    });

    const data = await response.json();

    hideTyping();
    addMessage("bot", data.reply);

  } catch (error) {
    hideTyping();
    addMessage("bot", "Sorry, something went wrong. Please try again.");
  }

  loading = false;
  sendButton.disabled = false;
  inputBox.focus();
}


function quickSend(text) {
  inputBox.value = text;
  sendMessage();
}


inputBox.addEventListener("keydown", function(e) {
  if (e.key === "Enter") sendMessage();
});