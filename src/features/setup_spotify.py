# src/features/setup_spotify.py
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

def setup_spotify():
    """Initialize Spotify client"""
    scope = [
        'user-library-read',
        'user-library-modify',
        'playlist-modify-public',
        'user-read-currently-playing',
        'user-top-read',
        'user-read-playback-state',
        'user-read-recently-played',
        'playlist-read-private',
        'playlist-read-collaborative'
    ]
    return spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=os.getenv('SPOTIFY_CLIENT_ID'),
        client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
        redirect_uri=os.getenv('SPOTIFY_REDIRECT_URI'),
        scope=' '.join(scope)
    ))