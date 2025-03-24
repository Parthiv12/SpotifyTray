import os
import keyboard
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from winotify import Notification
import pystray
from PIL import Image
import threading
from src.core.spotify_client import SpotifyClient
from src.features.song_tracker import SongTracker
from src.utils.config import Config
import time
from src.features.playlist_manager import PlaylistManager

# Load environment variables
load_dotenv()

class SpotifyLiker:
    def __init__(self):
        self.spotify = SpotifyClient()
        self.tracker = SongTracker()
        self.config = Config()
        self.playlist_manager = PlaylistManager(self.spotify)
        self.setup_tray()
        self.setup_hotkeys()

    def send_notification(self, title, message):
        try:
            icon_path = os.path.abspath("spotify_liker_icon.png")
            toast = Notification(
                app_id="Spotify Liker",
                title=title,
                msg=message,
                duration="long",
                icon=icon_path,
                launch="",
                toast=None
            )
            toast.set_audio(sound=toast.Default, loop=False)
            toast.show()
            
            def check_and_resend():
                time.sleep(0.5)
                toast.show()
            
            threading.Thread(target=check_and_resend, daemon=True).start()
            
        except Exception as e:
            print(f"Notification error: {e}")

    def like_current_song(self):
        try:
            print("\n--- Debug Info ---")
            print("1. Getting current track...")
            
            # Try different methods to get the current track
            current_playback = self.spotify.sp.current_playback()
            print("Current playback:", current_playback)
            
            current_playing = self.spotify.sp.current_user_playing_track()
            print("Current playing track:", current_playing)
            
            # Use whichever method returns data
            current_track = current_playback or current_playing
            
            if current_track and current_track.get('item'):
                track_id = current_track['item']['id']
                track_name = current_track['item']['name']
                artist_name = current_track['item']['artists'][0]['name']
                
                print(f"2. Found track: {track_name} by {artist_name}")
                
                is_liked = self.spotify.is_track_liked(track_id)
                print(f"3. Track is liked: {is_liked}")
                
                if not is_liked:
                    if self.spotify.like_track(track_id):
                        self.tracker.add_liked_song(track_id, track_name, artist_name)
                        message = f"'{track_name}' by {artist_name}"
                        print(f"4. Successfully liked song: {message}")
                        self.send_notification("Song Liked! ❤️", message)
                else:
                    message = f"'{track_name}' is already in your liked songs!"
                    self.send_notification("Already Liked!", message)
            else:
                print("No track data found. Make sure:")
                print("- Spotify is running")
                print("- A song is currently playing (not paused)")
                print("- You're using the same Spotify account you authorized with")
                self.send_notification("No Song Playing", "Please play a song first")
        except Exception as e:
            print(f"Error: {e}")
            self.send_notification("Error", str(e))

    def unlike_current_song(self):
        try:
            current_track = self.spotify.get_current_track()
            if current_track and current_track.get('item'):
                track_id = current_track['item']['id']
                track_name = current_track['item']['name']
                artist_name = current_track['item']['artists'][0]['name']
                
                if self.spotify.is_track_liked(track_id):
                    if self.spotify.unlike_track(track_id):
                        self.tracker.remove_liked_song(track_id)
                        message = f"'{track_name}' by {artist_name}"
                        print(f"Unliked song: {message}")
                        self.send_notification("Song Unliked 💔", message)
                else:
                    message = f"'{track_name}' is not in your liked songs!"
                    self.send_notification("Not Liked!", message)
            else:
                self.send_notification("No Song Playing", "Please play a song first")
        except Exception as e:
            print(f"Error: {e}")
            self.send_notification("Error", str(e))

    def create_monthly_playlist(self):
        try:
            playlist_name = self.playlist_manager.create_monthly_playlist()
            if playlist_name:
                self.send_notification(
                    "Playlist Created! 📝",
                    f"Created playlist: {playlist_name}"
                )
            else:
                self.send_notification(
                    "Playlist Error ❌",
                    "No songs found for this month"
                )
        except Exception as e:
            self.send_notification("Error", str(e))

    def create_genre_playlists(self):
        try:
            playlists = self.playlist_manager.create_genre_playlists()
            if playlists:
                self.send_notification(
                    "Genre Playlists Created! 🎵",
                    f"Created {len(playlists)} genre-based playlists"
                )
            else:
                self.send_notification(
                    "Genre Playlists Error ❌",
                    "Could not create genre playlists"
                )
        except Exception as e:
            self.send_notification("Error", str(e))

    def setup_hotkeys(self):
        keyboard.add_hotkey(
            self.config.settings['hotkeys']['like_song'],
            self.like_current_song
        )
        keyboard.add_hotkey(
            self.config.settings['hotkeys']['unlike_song'],
            self.unlike_current_song
        )

    def create_icon(self):
        if os.path.exists("spotify_liker_icon.png"):
            return Image.open("spotify_liker_icon.png")
        else:
            icon_size = (32, 32)
            icon_color = (30, 215, 96)  # Spotify green
            return Image.new('RGB', icon_size, icon_color)

    def setup_tray(self):
        menu_items = [
            pystray.MenuItem("Spotify Liker", lambda: None, enabled=False),
            pystray.MenuItem("Like Song (Ctrl+Alt+7)", lambda: self.like_current_song()),
            pystray.MenuItem("Unlike Song (Ctrl+Alt+8)", lambda: self.unlike_current_song()),
            pystray.MenuItem("Create Monthly Playlist", lambda: self.create_monthly_playlist()),
            pystray.MenuItem("Create Genre Playlists", lambda: self.create_genre_playlists()),
            pystray.MenuItem("Exit", lambda icon: icon.stop())
        ]
        
        self.icon = pystray.Icon(
            "Spotify Liker",
            icon=self.create_icon(),
            menu=pystray.Menu(*menu_items)
        )

    def run(self):
        self.send_notification(
            "Spotify Liker Started",
            "Running in background\nCtrl+Alt+7 to like\nCtrl+Alt+8 to unlike"
        )
        self.icon.run()

if __name__ == "__main__":
    print("Starting Spotify Liker...")
    print("Use Ctrl+Alt+7 to like the current song")
    print("Use Ctrl+Alt+8 to unlike the current song")
    print("Check system tray for icon")
    
    app = SpotifyLiker()
    app.run()