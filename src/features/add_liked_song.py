# src/features/add_liked_song.py
def add_liked_song(conn, sp, track_id: str, name: str, artist: str):
    """Add song with enhanced metadata"""
    try:
        with conn:
            # Get track features from Spotify
            track_features = sp.audio_features(track_id)[0]
            track_info = sp.track(track_id)

            # Get artist genres
            artist_info = sp.artist(track_info['artists'][0]['id'])
            genres = artist_info['genres']
            primary_genre = genres[0] if genres else 'Unknown'

            conn.execute("""   
                INSERT OR REPLACE INTO liked_songs 
                (id, name, artist, genre, energy, danceability, tempo, acousticness)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (track_id, name, artist, primary_genre,
                  track_features['energy'], track_features['danceability'],
                  track_features['tempo'], track_features['acousticness']))
            return True
    except Exception as e:
        print(f"Error adding song to database: {e}")
        return False