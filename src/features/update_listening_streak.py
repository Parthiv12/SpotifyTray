# src/features/update_listening_streak.py
from datetime import datetime, timedelta

def update_listening_streak(conn):
    """Update listening streak tracking"""
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    # Get yesterday's streak
    cursor = conn.execute(
        "SELECT streak_count FROM listening_streaks WHERE date = ?",
        (yesterday.strftime('%Y-%m-%d'),)
    )
    yesterday_result = cursor.fetchone()
    yesterday_streak = yesterday_result[0] if yesterday_result else 0

    # Check if we already have an entry for today
    cursor = conn.execute(
        "SELECT streak_count FROM listening_streaks WHERE date = ?",
        (today.strftime('%Y-%m-%d'),)
    )
    today_result = cursor.fetchone()

    if not today_result:
        # No entry for today yet, create new one with incremented streak
        new_streak = yesterday_streak + 1 if yesterday_streak > 0 else 1
        conn.execute("""
            INSERT INTO listening_streaks (date, songs_played, streak_count)
            VALUES (?, 1, ?)
        """, (today.strftime('%Y-%m-%d'), new_streak))
    else:
        # Already have an entry for today, just increment songs_played
        conn.execute("""
            UPDATE listening_streaks 
            SET songs_played = songs_played + 1
            WHERE date = ?
        """, (today.strftime('%Y-%m-%d'),))

    conn.commit()