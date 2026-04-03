from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from predict import predict_mood, get_playlist

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

@app.get('/playlist/{mood}')
def playlist(mood: str):
    songs = get_playlist(mood)
    if not songs:
        raise HTTPException(status_code=404, detail=f"No playlist found for mood: {mood}")
    return {"mood": mood, "songs": songs}

