from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from predict import predict_mood, get_playlist
import random

app = FastAPI(
    title='Music Mood Classifier API',
    description='Predicts mood from audio features and returns playlists',
    version='1.0.0'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class AudioFeatures(BaseModel):
    danceability: float = Field(..., ge=0.0, le=1.0)
    energy: float = Field(..., ge=0.0, le=1.0)
    loudness: float = Field(..., ge=-60.0, le=0.0)
    speechiness: float = Field(..., ge=0.0, le=1.0)
    acousticness: float = Field(..., ge=0.0, le=1.0)
    instrumentalness: float = Field(..., ge=0.0, le=1.0)
    liveness: float = Field(..., ge=0.0, le=1.0)
    valence: float = Field(..., ge=0.0, le=1.0)
    tempo: float = Field(..., ge=0.0, le=250.0)
    popularity: float = Field(..., ge=0.0, le=100.0)
    duration_ms: float = Field(..., ge=0.0)

@app.get("/")
def root():
    return {"message": "Music Mood Classifier API is running 🎵 "}

@app.post("/predict")
def predict(features: AudioFeatures):
    try:
        result = predict_mood(features.model_dump())
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/playlist/{mood}")
def playlist(mood: str, confidence: float = 100.0):
    songs = get_playlist(mood)
    if not songs:
        raise HTTPException(status_code=404, detail=f"No playlist found for mood: {mood}")
    
    # High confidence → top popular songs
    # Low confidence → more randomness
    if confidence >= 90:
        # Small shuffle within top songs
        top = songs[:12]
        random.shuffle(top)
        result = top[:8]
    elif confidence >= 80:
        # Mix of popular and random
        top = songs[:10]
        random.shuffle(top)
        result = top[:8]
    else:
        # Full shuffle — anything goes
        shuffled = songs.copy()
        random.shuffle(shuffled)
        result = shuffled[:8]

    return {"mood": mood, "songs": result}

