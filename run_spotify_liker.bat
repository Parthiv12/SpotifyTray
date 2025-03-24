@echo off
echo Starting Spotify Liker...

:: Change to script directory
cd "%~dp0"

:: Create venv if it doesn't exist
if not exist .venv (
    echo Creating virtual environment...
    python -m venv .venv
    
    :: Activate venv and install requirements
    call .venv\Scripts\activate
    pip install -r requirements.txt
) else (
    :: Just activate existing venv
    call .venv\Scripts\activate
)

:: Run the application with venv's pythonw
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