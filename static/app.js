const voiceState = {
  sessionId: null,
};

const sessionState = document.querySelector("#session-state");
const responsePanel = document.querySelector("#response-panel");
const emptyState = document.querySelector("#empty-state");
const responseText = document.querySelector("#response-text");
const meta = document.querySelector("#meta");
const sources = document.querySelector("#sources");
const transcriptLog = document.querySelector("#transcript-log");
const sessionChip = document.querySelector("#session-chip");
const recentSessions = document.querySelector("#recent-sessions");

const kpiActive = document.querySelector("#kpi-active");
const kpiTurns = document.querySelector("#kpi-turns");
const kpiEscalations = document.querySelector("#kpi-escalations");
const kpiArticles = document.querySelector("#kpi-articles");

async function loadDashboard() {
  const response = await fetch("/api/dashboard");
  const data = await response.json();
  kpiActive.textContent = data.active_sessions;
  kpiTurns.textContent = data.total_turns;
  kpiEscalations.textContent = data.total_escalations;
  kpiArticles.textContent = data.knowledge_articles;

  recentSessions.innerHTML = "";
  if (!data.recent_sessions.length) {
    recentSessions.innerHTML = "<p class=\"muted\">No sessions yet. Create one from the simulator.</p>";
    return;
  }

  data.recent_sessions.forEach((session) => {
    const item = document.createElement("article");
    item.className = "session-card";
    item.innerHTML = `
      <div class="session-head">
        <div>
          <strong>${session.caller_name}</strong>
          <div class="session-meta">${session.phone_number}</div>
        </div>
        <span class="status-badge ${session.escalation_required ? "escalated" : "normal"}">
          ${session.escalation_required ? "Escalated" : "Active"}
        </span>
      </div>
      <div class="session-meta">Session ${session.session_id}</div>
      <div class="session-meta">Turns: ${session.turn_count}${session.latest_intent ? ` | Intent: ${session.latest_intent}` : ""}</div>
    `;
    recentSessions.appendChild(item);
  });
}

function renderSources(sourceItems) {
  sources.innerHTML = "";
  if (!sourceItems.length) {
    sources.innerHTML = "<span class=\"source-pill\">No grounding source used</span>";
    return;
  }
  sourceItems.forEach((source) => {
    const item = document.createElement("span");
    item.className = "source-pill";
    item.textContent = `${source.title} • ${source.topic}`;
    sources.appendChild(item);
  });
}

function renderTimeline(turns) {
  transcriptLog.innerHTML = "";
  turns.forEach((turn) => {
    const item = document.createElement("article");
    item.className = `timeline-item ${turn.speaker}`;
    item.innerHTML = `
      <span class="timeline-label">${turn.speaker}</span>
      <div>${turn.text}</div>
    `;
    transcriptLog.appendChild(item);
  });
}

document.querySelectorAll(".prompt-pill").forEach((button) => {
  button.addEventListener("click", () => {
    document.querySelector("#transcript").value = button.dataset.prompt;
  });
});

document.querySelector("#session-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  const callerName = document.querySelector("#caller-name").value;
  const phoneNumber = document.querySelector("#phone-number").value;

  const response = await fetch("/api/session", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ caller_name: callerName, phone_number: phoneNumber }),
  });
  const data = await response.json();
  voiceState.sessionId = data.session_id;
  sessionState.textContent = `Session ${data.session_id} created. Greeting: ${data.greeting}`;
  sessionChip.textContent = `Active Session ${data.session_id}`;
  await loadDashboard();
});

document.querySelector("#transcript-form").addEventListener("submit", async (event) => {
  event.preventDefault();
  if (!voiceState.sessionId) {
    sessionState.textContent = "Create a session first.";
    return;
  }

  const transcript = document.querySelector("#transcript").value;
  const response = await fetch("/api/respond", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ session_id: voiceState.sessionId, transcript }),
  });
  const data = await response.json();
  emptyState.classList.add("hidden");
  responsePanel.classList.remove("hidden");
  responseText.textContent = data.response_text;
  meta.textContent = `Intent: ${data.intent} | Sentiment: ${data.sentiment} | Escalation: ${data.escalation_required ? "required" : "not required"}`;
  renderSources(data.sources || []);
  renderTimeline(data.transcript || []);
  await loadDashboard();
});

document.querySelector("#refresh-dashboard").addEventListener("click", loadDashboard);

loadDashboard();
