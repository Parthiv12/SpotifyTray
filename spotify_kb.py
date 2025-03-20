import os
import spotipy
import keyboard
from spotipy.oauth2 import SpotifyOAuth
from winotify import Notification
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API credentials from .env
SPOTIPY_CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
SPOTIPY_CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIFY_REDIRECT_URI')
SCOPE = 'user-library-modify user-library-read user-read-currently-playing'

# Initialize Spotify client
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=SPOTIPY_CLIENT_ID,
    client_secret=SPOTIPY_CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
    scope=SCOPE
))

def send_notification(title, message):
    """Shows a Windows notification."""
    toast = Notification(
        app_id="Spotify Liker",
        title=title,
        msg=message,
        duration="short"
    )
    toast.show()

def like_current_song():
    try:
        current_track = sp.current_user_playing_track()
        if current_track and current_track['item']:
            track_id = current_track['item']['id']
            track_name = current_track['item']['name']
            artist_name = current_track['item']['artists'][0]['name']
            
            is_liked = sp.current_user_saved_tracks_contains([track_id])[0]
            
            if not is_liked:
                sp.current_user_saved_tracks_add([track_id])
                message = f"'{track_name}' by {artist_name}"
                print(f"Liked song: {message}")
                send_notification("Song Liked! ❤️", message)
            else:
                message = f"'{track_name}' is already in your liked songs!"
                send_notification("Already Liked!", message)
        else:
            send_notification("No Song Playing", "Please play a song first")
    except Exception as e:
        send_notification("Error", str(e))
        print(f"Error: {e}")

def unlike_current_song():
    try:
        current_track = sp.current_user_playing_track()
        if current_track and current_track['item']:
            track_id = current_track['item']['id']
            track_name = current_track['item']['name']
            artist_name = current_track['item']['artists'][0]['name']
            
            is_liked = sp.current_user_saved_tracks_contains([track_id])[0]
            
            if is_liked:
                sp.current_user_saved_tracks_delete([track_id])
                message = f"'{track_name}' by {artist_name}"
                print(f"Unliked song: {message}")
                send_notification("Song Unliked 💔", message)
            else:
                message = f"'{track_name}' is not in your liked songs!"
                send_notification("Not Liked!", message)
        else:
            send_notification("No Song Playing", "Please play a song first")
    except Exception as e:
        send_notification("Error", str(e))
        print(f"Error: {e}")

# Set up hotkeys
keyboard.add_hotkey("ctrl+alt+7", like_current_song)    # Like song
keyboard.add_hotkey("ctrl+alt+8", unlike_current_song)  # Unlike song

if __name__ == "__main__":
    print("Spotify Song Liker is running...")
    print("Use Ctrl+Alt+7 to like the current song")
    print("Use Ctrl+Alt+8 to unlike the current song")
    print("Press Ctrl+C to exit")
    
    # Keep the program running
    keyboard.wait()
