# src/features/create_auto_playlist.py
def create_auto_playlist(conn, sp, playlist_type: str = 'weekly'):
    """Create automatic playlist based on listening history"""
    if playlist_type == 'weekly':
        time_range = '7 days'
        playlist_name = 'Weekly Favorites'
    else:
        time_range = '30 days'
        playlist_name = 'Monthly Favorites'

    # Get recently liked songs
    df = pd.read_sql("""
        SELECT id, name, artist
        FROM liked_songs
        WHERE timestamp >= datetime('now', ?)
        ORDER BY timestamp DESC
    """, conn, params=(f'-{time_range}',))

    if df.empty:
        return False

    # Create playlist
    user_id = sp.current_user()['id']
    playlist = sp.user_playlist_create(
        user_id,
        playlist_name,
        public=True,
        description=f'Auto-generated {playlist_type} playlist'
    )

    # Add tracks to playlist
    sp.playlist_add_items(playlist['id'], df['id'].tolist())

    # Save playlist info to database
    conn.execute("""
        INSERT INTO playlists (id, name, type)
        VALUES (?, ?, ?)
    """, (playlist['id'], playlist_name, playlist_type))
    conn.commit()

    return True