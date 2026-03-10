# Current Goal: Get python to successfully play one local music file

# import required modules
import vlc
import time 
from pathlib import Path

def list_files_pathlib(directory):
    return[str(file) for file in Path(directory).iterdir() if file.is_file()]

def main():

    # Create instance of player
    instance = vlc.Instance()

    # Create media list player
    player = instance.media_list_player_new()

    # Create a media list
    path_to_album = "/Users/jordan/Music/tyler_the_creator/dont_tap_the_glass/"
    album_list = list_files_pathlib(path_to_album)
    media_list = instance.media_list_new(album_list)

    player.set_media_list(media_list)

    player.play()

    try
        while player.is_playing():
            time.sleep(1)
    except KeyboardInterrupt:
        player.stop()

main()
