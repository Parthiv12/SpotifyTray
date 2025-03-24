# src/features/schedule_auto_playlists.py
import schedule
import time

def schedule_auto_playlists(create_auto_playlist):
    """Schedule automatic playlist creation"""
    # Create weekly playlist every Sunday at midnight
    schedule.every().sunday.at("00:00").do(
        create_auto_playlist, playlist_type='weekly'
    )

    # Create monthly playlist on the 1st of each month
    schedule.every().day.at("00:00").do(
        lambda: create_auto_playlist('monthly') if datetime.now().day == 1 else None
    )

    while True:
        schedule.run_pending()
        time.sleep(60)