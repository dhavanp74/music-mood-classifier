import joblib
import numpy as np
import json

model = joblib.load('mood_model.pkl')
scaler = joblib.load('scaler.pkl')
pca = joblib.load('pca.pkl')

with open('playlist_data.json', 'r') as f:
    playlist_data = json.load(f)

FEATURE_ORDER = [
    'danceability', 'energy', 'loudness', 'speechiness',
    'acousticness', 'instrumentalness', 'liveness',
    'valence', 'tempo', 'popularity', 'duration_ms'
]

MOOD_EMOJI = {
    'Happy':     '😊',
    'Sad':       '😢',
    'Energetic': '⚡',
    'Calm':      '😌',
    'Neutral':   '😐'
}

def predict_mood(features: dict) -> dict:
    input_array = np.array([[features[f] for f in FEATURE_ORDER]])

    scaled = scaler.transform(input_array)
    pca_input = pca.transform(scaled)

    mood = model.predict(pca_input)[0]
    probabilities = model.predict_proba(pca_input)[0]
    confidence = round(float(max(probabilities)) * 100, 2)

    return {
        'mood': mood,
        'emoji': MOOD_EMOJI[mood],
        'confidence': confidence
    } 


def get_playlist(mood: str) -> list:
    mood = mood.capitalize()
    if mood not in playlist_data:
        return []
    return playlist_data[mood]


