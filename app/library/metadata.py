# Current Goal: Return song info based on list of songs given

from pathlib import Path 
from mutagen import File
from mutagen.easyid3 import EasyID3
from scanner import scan



"""
 Sudo code steps:
    1. Get list of songs
    2. For each song get metadata and store in new list
"""

metadata_list = []

def extract_metadata(path):
    try:
        audio = File(path, easy=True)

        return {
            "path": path,
            "album": audio.get("album", [None])[0],
            "title": audio.get("title", [None])[0],
            "artist": audio.get("artist", [None])[0],
            "duration": audio.info.length
        }
    except Exception as e:
        print(f"Failed to read metadata for {path}: {e}")
        return None


data = extract_metadata("/Users/jordan/Music/tyler_the_creator/dont_tap_the_glass/01.flac")

print(data)
