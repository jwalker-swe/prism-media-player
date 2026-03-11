# Current Goal: Return file paths of all files in defined root directory

from pathlib import Path

def scan(directory):

    # Define supported file types
    SUPPORTED = {".mp3", ".wav", ".flac", ".aac"}

    # Fetch all songs within definied root directory
    songs = [
            str(file)
            for file in Path(directory).rglob("*")
            if file.is_file() and file.suffix.lower() in SUPPORTED
            ]

    if songs:
        return songs
    else:
        return None


# Run scan and create list of called songs

