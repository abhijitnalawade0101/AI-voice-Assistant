// 🎤 Handle voice input
async function fetchVoiceChat() {
  try {
    document.getElementById("user-query").innerText = "🎙️ Listening...";
    document.getElementById("ai-reply").innerText = "🤖 Thinking...";

    const res = await fetch("http://localhost:8000/voice-chat");
    const data = await res.json();

    const userText = data.spoken_query;
    const aiText = data.ai_reply;

    document.getElementById("user-query").innerText = "🧑 You said: " + userText;
    document.getElementById("ai-reply").innerText = "🤖 AI says: " + aiText;

    appendToHistory(userText, aiText);
  } catch (error) {
    console.error("Error:", error);
    document.getElementById("user-query").innerText = "voice bot is working.";
    document.getElementById("ai-reply").innerText = "Please wait it will take time";
  }
}

// ⌨️ Handle text input
async function handleTextCommand() {
  const input = document.getElementById("text-command").value.trim();
  if (!input) return;

  document.getElementById("user-query").innerText = "🧑 You typed: " + input;
  document.getElementById("ai-reply").innerText = "🤖 Thinking...";

  try {
    const res = await fetch("http://localhost:8000/text-chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query: input })
    });

    const data = await res.json();
    const aiText = data.ai_reply;

    document.getElementById("ai-reply").innerText = "🤖 AI says: " + aiText;

    appendToHistory(input, aiText);
  } catch (err) {
    console.error(err);
    document.getElementById("ai-reply").innerText = "⚠️ Error talking to AI.";
  }

  document.getElementById("text-command").value = "";
  autoResize(document.getElementById("text-command"));
}

// 🧭 Add history entry in sidebar and handle click
function appendToHistory(userInput, aiReply) {
  const historyBox = document.getElementById("search-history");

  const entry = document.createElement("div");
  entry.classList.add("history-entry");

  // Show only part of input in sidebar
  entry.textContent = userInput.length > 50 ? userInput.slice(0, 50) + "..." : userInput;

  // On click: show full in main view
  entry.addEventListener("click", () => {
    document.getElementById("user-query").innerText = "🧑 You typed: " + userInput;
    document.getElementById("ai-reply").innerText = "🤖 AI says: " + aiReply;
  });

  historyBox.prepend(entry); // newest first
}

// ⬆️ Auto-grow textarea
function autoResize(textarea) {
  textarea.style.height = 'auto';
  textarea.style.height = textarea.scrollHeight + 'px';
}
