import os
import spotipy
import keyboard
from spotipy.oauth2 import SpotifyOAuth
from winotify import Notification
from dotenv import load_dotenv
import pystray
from PIL import Image
import threading
import winshell
from win32com.client import Dispatch
import sys

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
    try:
        # Get the absolute path to the icon
        icon_path = os.path.abspath("spotify_liker_icon.png")
        
        toast = Notification(
            app_id="Spotify Liker",
            title=title,
            msg=message,
            duration="short",  # Make notification stay longer
            icon=icon_path
        )
        toast.show()
        
    except Exception as e:
        print(f"Notification error: {e}")

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
                message = f"Track: {track_name}\nArtist: {artist_name}"  # More detailed message
                print(f"Liked song: {message}")
                send_notification("♥️ Song Added to Liked Songs! ♥️", message)  # More visible title
            else:
                message = f"Track: {track_name}\nArtist: {artist_name}"
                send_notification("Already in Liked Songs ✨", message)
        else:
            send_notification("⚠️ No Song Playing", "Please play a song first")
    except Exception as e:
        send_notification("❌ Error", str(e))
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
                message = f"Track: {track_name}\nArtist: {artist_name}"
                print(f"Unliked song: {message}")
                send_notification("💔 Song Removed from Liked Songs 💔", message)
            else:
                message = f"Track: {track_name}\nArtist: {artist_name}"
                send_notification("Not in Liked Songs ❌", message)
        else:
            send_notification("⚠️ No Song Playing", "Please play a song first")
    except Exception as e:
        send_notification("❌ Error", str(e))
        print(f"Error: {e}")

def get_icon():
    """Load the custom icon."""
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spotify_liker_icon.png")
    if os.path.exists(icon_path):
        return Image.open(icon_path)
    else:
        # Fallback to a colored icon if custom icon is not found
        icon_size = (32, 32)
        icon_color = (30, 215, 96)  # Spotify green
        return Image.new('RGB', icon_size, icon_color)

def setup_tray():
    icon = pystray.Icon(
        "Spotify Liker",
        icon=get_icon(),
        menu=pystray.Menu(
            pystray.MenuItem("Spotify Liker", lambda: None, enabled=False),
            pystray.MenuItem("Like Song (Ctrl+Alt+7)", lambda: None, enabled=False),
            pystray.MenuItem("Unlike Song (Ctrl+Alt+8)", lambda: None, enabled=False),
            pystray.MenuItem("Exit", lambda icon: icon.stop())
        )
    )
    return icon

def run_keyboard_listener():
    keyboard.add_hotkey("ctrl+alt+7", like_current_song)
    keyboard.add_hotkey("ctrl+alt+8", unlike_current_song)
    keyboard.wait()

def create_startup_shortcut():
    try:
        startup_folder = winshell.startup()
        script_path = os.path.abspath(__file__)
        pythonw_path = os.path.join(os.path.dirname(sys.executable), 'pythonw.exe')
        
        shortcut_path = os.path.join(startup_folder, "Spotify Liker.lnk")
        
        shell = Dispatch('WScript.Shell')
        shortcut = shell.CreateShortCut(shortcut_path)
        shortcut.Targetpath = pythonw_path
        shortcut.Arguments = f'"{script_path}"'
        shortcut.WorkingDirectory = os.path.dirname(script_path)
        shortcut.save()
        
        print("✅ Startup shortcut created successfully!")
        print(f"The script will now start automatically when Windows starts")
    except Exception as e:
        print(f"❌ Error creating startup shortcut: {e}")

def main():
    # Start keyboard listener in a separate thread
    keyboard_thread = threading.Thread(target=run_keyboard_listener, daemon=True)
    keyboard_thread.start()
    
    # Create and run system tray icon
    icon = setup_tray()
    
    # Show startup notification
    send_notification(
        "Spotify Liker Started",
        "Running in background\nCtrl+Alt+7 to like\nCtrl+Alt+8 to unlike"
    )
    
    # Run the system tray icon
    icon.run()

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--setup":
        create_startup_shortcut()
    else:
        main()