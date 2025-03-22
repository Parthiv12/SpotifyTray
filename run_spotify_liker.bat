@echo off
echo Starting Spotify Liker...
cd "%~dp0"
.venv\Scripts\pythonw.exe spotify_kb.py
if errorlevel 1 (
    echo Error starting Spotify Liker
    .venv\Scripts\python.exe spotify_kb.py
    pause
) 

def track_listening_habits():
    """Track and visualize your music taste"""
    # Store liked songs in SQLite database
    # Generate graphs of favorite genres
    # Show listening patterns over time 

def get_smart_recommendations():
    """Use AI to suggest similar songs"""
    # Analyze audio features
    # Use machine learning for recommendations
    # Consider time of day/activity 