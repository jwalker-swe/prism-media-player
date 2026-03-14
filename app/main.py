from app.db.database import init_db
from app.library.scanner import scan
from app.library.metadata import extract_metadata
from app.db.repository import insert_tracks
from app.db.repository import get_all_tracks
from app.db.repository import search_tracks
from app.playback.controller import MusicController

MUSIC_LIBRARY_PATH = "/Users/jordan/Music/library/"

def main():
    init_db()
    paths = scan(MUSIC_LIBRARY_PATH)
    metadata_list = [
        extract_metadata(path) for path in paths
    ]
    insert_tracks(metadata_list)

    all_available_tracks = get_all_tracks()

    search_results = search_tracks("tyler")

    print(f"Searched Tracks: {search_results}")
    

if __name__ == "__main__":
    main()
