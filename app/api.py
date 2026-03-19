from pydantic import BaseModel
from fastapi import FastAPI, APIRouter
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.db.repository import get_all_tracks, search_tracks
from app.playback.controller import MusicController

class Track(BaseModel):
    id: int
    path: str
    title: str
    artist: str
    album: str
    tracknumber: int
    duration: float

app = FastAPI()
controller = MusicController()
router = APIRouter(prefix="/api")

@router.get("/library")
def get_library():
    return get_all_tracks()

@router.get("/search")
def search(q: str):
    return search_tracks(q)

@router.post("/play")
def play():
    controller.play()

@router.post("/pause")
def pause():
    controller.pause()

@router.post("/resume")
def resume():
    controller.resume()

@router.post("/next")
def next_track():
    controller.next_track()

@router.post("/prev")
def previous_track():
    controller.prev_track()

@router.post("/queue/add")
def add_to_queue(track: Track):
    controller.add_to_queue(dict(track))

@router.post("/queue/clear")
def clear_queue():
    controller.clear_queue()

@router.get("/queue")
def get_queue():
    return controller.get_queue()

app.include_router(router)

app.mount("/", StaticFiles(directory="frontend/dist", html=True), name="static")
