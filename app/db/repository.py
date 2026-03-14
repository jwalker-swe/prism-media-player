"""
Current Goals: 

Implement the three following functions
    x insert_track(metadata_dict)
        - insert or ignore if path already exists ( use INSERT OR IGNORE )

    x get_all_tracks()
        - return all rows

    - search_tracks(query)
        - WHERE title LIKE ? OR artist LIKE ? OR album LIKE ?
"""

import sqlite3
from app.db.database import define_connection


def insert_tracks(metadata_list):
    conn = define_connection()
    cursor = conn.cursor()

    try:
        for metadata in metadata_list:
            # Convert metadata tracknumber data to int before storing to db
            tracknumber = metadata["tracknumber"]
            if tracknumber:
                tracknumber = int(str(tracknumber).split("/")[0])

            cursor.execute(
                """
                    INSERT OR IGNORE INTO tracks (
                        path,
                        title,
                        artist,
                        album,
                        tracknumber,
                        duration
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """,
                (metadata["path"], 
                 metadata["title"],
                 metadata["artist"],
                 metadata["album"],
                 # insert converted tracknumber value from above instead of original metadata tracknumber value
                 tracknumber,
                 metadata["duration"]
                )
            )

        conn.commit()
        conn.close()

        print("Successfully inserted tracks to db")
    
    except Exception as e:
        print(f"Failed to insert tracks to db: {e}")


def get_all_tracks():
    conn = define_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tracks")

    tracks = [dict(row) for row in cursor.fetchall()]
    sorted_tracks = sorted(tracks, key=lambda x: x["tracknumber"])

    
    return sorted_tracks

def search_tracks(query):
    conn = define_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    like = f"%{query}%"
    cursor.execute(
        """
            SELECT * FROM tracks
            WHERE title LIKE ?
            OR artist LIKE ?
            OR album LIKE ?
        """,
        (like, like, like)
    )

    return [dict(row) for row in cursor.fetchall()]
