# src/features/enhanced_song_tracker.py
import os
from threading import Lock
from .load_config import load_config
from .setup_spotify import setup_spotify
from .setup_database import setup_database
from .add_liked_song import add_liked_song
from .update_listening_streak import update_listening_streak
from .get_listening_streak import get_listening_streak
from .generate_heatmap import generate_heatmap
from .get_recommendations import get_recommendations
from .create_auto_playlist import create_auto_playlist
from .analyze_genres import analyze_genres
from .create_dashboard import create_dashboard
from .schedule_auto_playlists import schedule_auto_playlists
from .setup_keyboard_shortcuts import setup_keyboard_shortcuts
from .check_access_token import check_access_token
from .create_dashboard import create_dashboard

class EnhancedSongTracker:
    def __init__(self):
        self.db_path = os.path.join('data', 'database.sqlite')
        os.makedirs('data', exist_ok=True)
        self.db_lock = Lock()
        self.conn = setup_database(self.db_path)
        self.config = load_config()
        self.sp = setup_spotify()
        
    # ... rest of the class methods, using the imported functions ...