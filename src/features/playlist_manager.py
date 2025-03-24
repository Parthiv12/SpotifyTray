from datetime import datetime
from typing import List, Optional, Dict

class PlaylistManager:
    def __init__(self, spotify_client):
        self.sp = spotify_client
        
    def create_monthly_playlist(self) -> Optional[str]:
        """Create a playlist of monthly liked songs"""
        try:
            month = datetime.now().strftime('%B %Y')
            playlist_name = f"Liked Songs - {month}"
            
            # Create new playlist
            playlist = self.sp.create_playlist(
                name=playlist_name,
                description=f"Songs liked during {month}",
                public=False
            )
            
            if playlist:
                # Get this month's liked songs
                liked_songs = self.get_monthly_liked_songs()
                if liked_songs:
                    track_uris = [song['uri'] for song in liked_songs]
                    self.sp.add_tracks_to_playlist(playlist['id'], track_uris)
                    return playlist_name
            return None
            
        except Exception as e:
            print(f"Error creating monthly playlist: {e}")
            return None
    
    def get_monthly_liked_songs(self) -> List[Dict]:
        """Get all songs liked in the current month"""
        try:
            all_tracks = self.sp.get_monthly_liked_songs()
            current_month = datetime.now().month
            current_year = datetime.now().year
            
            # Filter for current month
            monthly_tracks = []
            for track in all_tracks:
                added_at = datetime.strptime(track['added_at'], '%Y-%m-%dT%H:%M:%SZ')
                if added_at.month == current_month and added_at.year == current_year:
                    monthly_tracks.append(track)
                
            return monthly_tracks
            
        except Exception as e:
            print(f"Error getting monthly liked songs: {e}")
            return []

    def create_genre_playlists(self) -> List[str]:
        """Create playlists based on genres"""
        try:
            # Get all liked songs
            tracks = self.sp.get_monthly_liked_songs()
            
            # Group by genre
            genre_tracks = {}
            for track in tracks:
                track_info = self.sp.get_track_info(track['uri'].split(':')[-1])
                if track_info:
                    artist_id = track_info['artists'][0]['id']
                    artist_info = self.sp.sp.artist(artist_id)
                    genres = artist_info['genres']
                    
                    for genre in genres:
                        if genre not in genre_tracks:
                            genre_tracks[genre] = []
                        genre_tracks[genre].append(track['uri'])
            
            # Create playlists for each genre
            created_playlists = []
            for genre, tracks in genre_tracks.items():
                if len(tracks) >= 5:  # Only create if we have enough songs
                    playlist = self.sp.create_playlist(
                        name=f"Liked - {genre.title()}",
                        description=f"Your liked {genre} songs",
                        public=False
                    )
                    if playlist:
                        self.sp.add_tracks_to_playlist(playlist['id'], tracks)
                        created_playlists.append(playlist['name'])
            
            return created_playlists
            
        except Exception as e:
            print(f"Error creating genre playlists: {e}")
            return []

    def get_current_track(self) -> Optional[Dict]:
        try:
            print("\nTrying to get current track...")
            # First attempt using playback state
            current = self.sp.current_playback()
            print("Current playback state:", current)
            
            # Fallback attempt if first method fails
            if not current:
                print("Trying alternative method...")
                current = self.sp.current_user_playing_track()
            return current
        except Exception as e:
            print(f"Error getting current track: {e}")
            return None 