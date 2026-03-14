import vlc
import sqlite3
from app.db.databse import definte_connection 

# Create class for controller
# should contain methods such as play, pause, stop, next_track,
# prev_track get_current_track and returns the track info of the
# currently track being played

class MusicController:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_list_player_new()
        self.media_list = None

    def play(track_list):
        self.media_list = self.instance.media_list_player_new(track_list)
        self.player.set_media_list(self.media_list)        
        self.player.play()

    def pause()
        self.player.set_pause(1)

    def resume()
        self.player.set_pause(0)

    def stop()

    def next_track()
        self.player.next()

    def prev_track()
        self.player.previous()

    def get_current_track()
        media_player = self.player.get_media_player()
        media = media_player.get_media()

        if media:
            current_track_path = media.get_mrl()

            conn = definte_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                    SELECT * FROM tracks 
                    WHERE path IS ?
                """
            ), (current_track_path) 
            
        return cursor.fetchall(
        

    # Test all methods
