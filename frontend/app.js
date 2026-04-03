const API = "http://127.0.0.1:8000";

// Live slider value updates
const sliders = [
  "danceability","energy","valence","acousticness",
  "speechiness","instrumentalness","liveness",
  "tempo","loudness","popularity","duration_ms"
];

sliders.forEach(id => {
  const input = document.getElementById(id);
  const display = document.getElementById(`${id}-val`);
  input.addEventListener("input", () => display.textContent = input.value);
});

async function predictMood() {
  const btn = document.getElementById("predict-btn");
  btn.disabled = true;
  btn.textContent = "⏳ Predicting...";

  const payload = {};
  sliders.forEach(id => {
    payload[id] = parseFloat(document.getElementById(id).value);
  });

  try {
    // Step 1 — Predict mood
    const predRes = await fetch(`${API}/predict`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload)
    });
    const predData = await predRes.json();

    // Show result section
    document.getElementById("result-section").classList.remove("hidden");
    document.getElementById("mood-emoji").textContent  = predData.emoji;
    document.getElementById("mood-label").textContent  = predData.mood;
    document.getElementById("confidence-text").textContent = `${predData.confidence}%`;

    // Animate confidence bar
    setTimeout(() => {
      document.getElementById("confidence-fill").style.width = `${predData.confidence}%`;
    }, 100);

    // Step 2 — Fetch playlist
    const playRes = await fetch(`${API}/playlist/${predData.mood}?confidence=${predData.confidence}`);
    const playData = await playRes.json();

    // Render songs
    const grid = document.getElementById("songs-grid");
    grid.innerHTML = "";
    playData.songs.forEach(song => {
      grid.innerHTML += `
        <div class="song-card">
          <div class="track" title="${song.track_name}">${song.track_name}</div>
          <div class="artist" title="${song.artists}">${song.artists}</div>
          <div class="popularity">⭐ Popularity: ${song.popularity}</div>
        </div>`;
    });

    document.getElementById("playlist-section").classList.remove("hidden");

  } catch (err) {
    alert("Error connecting to API. Make sure the backend is running.");
    console.error(err);
  } finally {
    btn.disabled = false;
    btn.textContent = "🎯 Predict Mood";
  }
}