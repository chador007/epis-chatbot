const API_URL = "http://172.19.9.235:9000/chat";

const sendBtn = document.getElementById("sendBtn");
const input = document.getElementById("user-input");
const messages = document.getElementById("chat-messages");

marked.setOptions({
  breaks: true, // Convert \n to <br>
  gfm: true, // GitHub Flavored Markdown (tables, strikethrough)
  sanitize: false,
});

function closeChat() {
  window.parent.postMessage("epis:close", "*");
}

/* MESSAGE HELPERS */

function addDateChip(label) {
  const chip = document.createElement("div");
  chip.className = "date-chip";
  chip.textContent = label;
  messages.appendChild(chip);
}

function addUserMessage(text) {
  const div = document.createElement("div");
  div.className = "message user";
  div.textContent = text; // User messages stay as plain text (safe)
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return div;
}

function addBotMessage(text) {
  const div = document.createElement("div");
  div.className = "message bot";
  div.innerHTML = marked.parse(text); // ← Parse Markdown to HTML
  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
  return div;
}

/* TYPING */

function showTypingDots() {
  const div = document.createElement("div");

  div.id = "typingDots";
  div.className = "message bot typing-indicator";

  div.innerHTML =
    '<div class="typing-dot"></div>\
<div class="typing-dot"></div>\
<div class="typing-dot"></div>';

  messages.appendChild(div);
  messages.scrollTop = messages.scrollHeight;
}

function hideTypingDots() {
  const el = document.getElementById("typingDots");
  if (el) el.remove();
}

/* SEND MESSAGE */

sendBtn.addEventListener("click", sendMessage);

input.addEventListener("keydown", (e) => {
  if (e.key === "Enter") {
    e.preventDefault();
    sendMessage();
  }
});

async function sendMessage() {
  const text = input.value.trim();

  if (!text) return;

  addUserMessage(text);

  input.value = "";
  input.disabled = true;
  sendBtn.disabled = true;

  showTypingDots();

  try {
    const res = await fetch(API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        question: text,
        top_k: 5,
      }),
    });

    const data = await res.json();

    hideTypingDots();

    const reply = data.answer || "I couldn't retrieve that information.";

    addBotMessage(reply);
  } catch (err) {
    hideTypingDots();

    addBotMessage("⚠️ Unable to connect to ePIS services.");
  } finally {
    input.disabled = false;
    sendBtn.disabled = false;
    input.focus();
  }
}

addDateChip("Today");

addBotMessage(`
👋 **Welcome to ePIS!** I'm here to help you navigate the **Electronic Patient Information System (EPIS)**.

**I can assist you with:**
* 📁 Navigation and menu paths
* 🔧 Troubleshooting errors and access issues
* 📋 Step-by-step procedures for clinical and administrative tasks
* 👥 Role-specific guidance (Doctors, Nurses, Pharmacists)

---

**To get started, simply tell me:**
* What module you need help with (e.g., Pharmacy, IPD, Reception)
* What task you're trying to complete

How can I help you with EPIS today?
`);
