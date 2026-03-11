# Current Goals:
"""
Current Goals: 

Implement the three following functions
    - insert_track(metadata_dict)
        - insert or ignore if path already exists ( use INSERT OR IGNORE )

    - get_all_tracks()
        - return all rows

    - search_tracks(query)
        - WHERE title LIKE ? OR artist LIKE ? OR album LIKE ?
"""

from app.db.database import define_connection


def insert_tracks(metadata_list):
    conn = define_connection()
    cursor = conn.cursor()

    try:
        for metadata in metadata_list:
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
                 metadata["tracknumber"],
                 metadata["duration"]
                )
            )

        conn.commit()
        conn.close()

        print("Successfully inserted tracks to db")
    
    except Exception as e:
        print(f"Failed to insert tracks to db: {e}")


