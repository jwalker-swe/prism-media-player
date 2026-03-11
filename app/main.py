from app.db.database import init_db
from app.library.scanner import scan
from app.library.metadata import extract_metadata
from app.db.repository import insert_tracks

MUSIC_LIBRARY_PATH = "/Users/jordan/Music/library/"

def main():
    init_db()
    paths = scan(MUSIC_LIBRARY_PATH)
    metadata_list = [
        extract_metadata(path) for path in paths
    ]
    insert_tracks(metadata_list)

    

if __name__ == "__main__":
    main()
