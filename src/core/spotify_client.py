import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from typing import Optional, Dict
from dotenv import load_dotenv

class SpotifyClient:
    def __init__(self):
        load_dotenv()
        self.auth_manager = SpotifyOAuth(
            client_id=os.getenv('SPOTIFY_CLIENT_ID'),
            client_secret=os.getenv('SPOTIFY_CLIENT_SECRET'),
            redirect_uri="http://localhost:8888/callback",  # Hardcode this
            scope="user-library-modify user-library-read user-read-currently-playing user-read-playback-state playlist-modify-private",
            open_browser=True  # This will open the auth page automatically
        )
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def get_current_track(self) -> Optional[Dict]:
        """Get the currently playing track"""
        try:
            print("\nTrying to get current track...")
            
            # Try to get current playback state
            current = self.sp.current_playback()
            print("Current playback state:", current)
            
            if not current:
                print("Trying alternative method...")
                current = self.sp.current_user_playing_track()
                print("Current playing track:", current)
            
            return current
        except Exception as e:
            print(f"Error getting current track: {e}")
            print("Token info:", self.auth_manager.get_cached_token())
            return None

    def like_track(self, track_id: str) -> bool:
        """Add a track to liked songs"""
        try:
            self.sp.current_user_saved_tracks_add([track_id])
            return True
        except Exception as e:
            print(f"Error liking track: {e}")
            return False

    def unlike_track(self, track_id: str) -> bool:
        """Remove a track from liked songs"""
        try:
            self.sp.current_user_saved_tracks_delete([track_id])
            return True
        except Exception as e:
            print(f"Error unliking track: {e}")
            return False

    def is_track_liked(self, track_id: str) -> bool:
        """Check if a track is in liked songs"""
        try:
            return self.sp.current_user_saved_tracks_contains([track_id])[0]
        except Exception as e:
            print(f"Error checking track status: {e}")
            return False

    def get_user_id(self) -> Optional[str]:
        """Get the current user's ID"""
        try:
            return self.sp.current_user()['id']
        except Exception as e:
            print(f"Error getting user ID: {e}")
            return None

    def create_playlist(self, name: str, description: str = "", public: bool = False) -> Optional[Dict]:
        """Create a new playlist"""
        try:
            user_id = self.get_user_id()
            if user_id:
                return self.sp.user_playlist_create(
                    user=user_id,
                    name=name,
                    public=public,
                    description=description
                )
            return None
        except Exception as e:
            print(f"Error creating playlist: {e}")
            return None

    def add_tracks_to_playlist(self, playlist_id: str, track_uris: list) -> bool:
        """Add tracks to a playlist"""
        try:
            # Add tracks in batches of 100 (Spotify API limit)
            for i in range(0, len(track_uris), 100):
                batch = track_uris[i:i + 100]
                self.sp.playlist_add_items(playlist_id, batch)
            return True
        except Exception as e:
            print(f"Error adding tracks to playlist: {e}")
            return False

    def get_track_info(self, track_id: str) -> Optional[Dict]:
        """Get detailed track information"""
        try:
            return self.sp.track(track_id)
        except Exception as e:
            print(f"Error getting track info: {e}")
            return None

    def get_monthly_liked_songs(self) -> list:
        """Get all tracks liked in the current month"""
        try:
            tracks = []
            results = self.sp.current_user_saved_tracks(limit=50)
            while results:
                for item in results['items']:
                    tracks.append({
                        'uri': item['track']['uri'],
                        'name': item['track']['name'],
                        'artist': item['track']['artists'][0]['name'],
                        'added_at': item['added_at']
                    })
                if results['next']:
                    results = self.sp.next(results)
                else:
                    break
            return tracks
        except Exception as e:
            print(f"Error getting liked songs: {e}")
            return [] 