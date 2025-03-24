# src/features/get_listening_streak.py
def get_listening_streak(conn) -> dict:
    """Get current listening streak information"""
    today = datetime.now().date()

    cursor = conn.execute(
        "SELECT streak_count, songs_played FROM listening_streaks WHERE date = ?",
        (today.strftime('%Y-%m-%d'),)
    )
    result = cursor.fetchone()

    if result:
        return {
            'current_streak': result[0],
            'songs_today': result[1]
        }
    return {'current_streak': 0, 'songs_today': 0}