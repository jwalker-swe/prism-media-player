import vlc
import sqlite3
from app.db.database import define_connection 

# Create class for controller
# should contain methods such as play, pause, stop, next_track,
# prev_track get_current_track and returns the track info of the
# currently track being played

class MusicController:
    def __init__(self):
        self.instance = vlc.Instance()
        self.player = self.instance.media_list_player_new()
        self.queue = []

    '''
    Setting up all methods for queue managment
    '''

    def add_to_queue(self, track):
        if len(self.queue) == 0:
            self.queue.append(track)
            self.player.play()
        else:
            self.queue.append(track)

    def remove_from_queue(self, index):
        self.queue.pop(index)

    def move_up(self, index):
        if index > 0:
            temp = self.queue[index]
            self.queue[index] = self.queue[index - 1]
            self.queue[index - 1] = temp

    def move_down(self, index):
        if index < len(self.queue):
            temp = self.queue[index]
            self.queue[index] = self.queue[index + 1]
            self.queue[index + 1] = temp

    def get_queue(self):
        return self.queue

    def clear_queue(self):
        self.queue.clear()
        self.player.stop()

    def play(self):
        paths = []
        for t in self.queue:
            paths.append(t["path"])

        media_list = self.instance.media_list_new()

        for path in paths:
            media_list.add_media(self.instance.media_new(path))

        self.player.set_media_list(media_list)
        self.player.play()

    def pause(self):
        self.player.set_pause(1)

    def resume(self):
        self.player.set_pause(0)

    def stop(self):
        self.player.stop()

    def next_track(self):
        self.player.next()

    def prev_track(self):
        self.player.previous()

    def get_current_track(self):
        from urllib.parse import unquote, urlparse

        media_player = self.player.get_media_player()
        media = media_player.get_media()

        if media:
            mrl = media.get_mrl()
            current_track_path = unquote(urlparse(mrl).path)

            conn = define_connection()
            cursor = conn.cursor()
            
            cursor.execute(
                """
                    SELECT * FROM tracks 
                    WHERE path IS ?
                """
            , (current_track_path, ) )
            
            return cursor.fetchone()



if __name__ == "__main__":
    import time
    from app.db.repository import get_all_tracks

    tracks = get_all_tracks()

    controller = MusicController()

    # Add tracks to queue
    for track in tracks:
        controller.add_to_queue(track)

    print("Queue:", [t["title"] for t in controller.get_queue()])


    # Print initial queue
    print("Initial queue:", [t["title"] for t in controller.get_queue()])

    # Test move_up — move track at index 2 up
    controller.move_up(2)
    print("After move_up(2):", [t["title"] for t in controller.get_queue()])

    # Test move_down — move track at index 0 down
    controller.move_down(0)
    print("After move_down(0):", [t["title"] for t in controller.get_queue()])

    # Test remove_from_queue — remove track at index 1
    controller.remove_from_queue(1)
    print("After remove(1):", [t["title"] for t in controller.get_queue()])

    # Test clear_queue
    controller.clear_queue()
    print("After clear:", controller.get_queue())  # should print []

    # Re-add tracks before playing
    for track in tracks:
        controller.add_to_queue(track)


    print("Playing...")
    controller.play()
    time.sleep(3)

    print("Current track:", controller.get_current_track())

    print("Pausing...")
    controller.pause()
    time.sleep(2)

    print("Resuming...")
    controller.resume()
    time.sleep(3)

    print("Next track...")
    controller.next_track()
    time.sleep(3)

    print("Current track:", controller.get_current_track())

    print("Previous track...")
    controller.prev_track()
    time.sleep(3)

    print("Stopping.")
    controller.stop()


# Test all methods
