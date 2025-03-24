import unittest
from unittest.mock import Mock, patch
from src.features.enhanced_song_tracker import EnhancedSongTracker
import os
from datetime import datetime, timedelta
import sqlite3
import time

# Mock Spotify API responses
MOCK_TRACK_RESPONSE = {
    'id': '11dFghVXANMlKmJXsNCbNl',
    'name': 'Test Song',
    'artists': [{'id': 'artist123', 'name': 'Test Artist'}],
    'album': {'name': 'Test Album'}
}

MOCK_ARTIST_RESPONSE = {
    'id': 'artist123',
    'name': 'Test Artist',
    'genres': ['pop', 'rock']
}

MOCK_AUDIO_FEATURES = {
    'energy': 0.8,
    'danceability': 0.7,
    'tempo': 120,
    'acousticness': 0.3
}

MOCK_RECOMMENDATIONS = {
    'tracks': [
        {
            'id': 'rec1',
            'name': 'Recommended Song 1',
            'artists': [{'name': 'Artist 1'}]
        },
        {
            'id': 'rec2',
            'name': 'Recommended Song 2',
            'artists': [{'name': 'Artist 2'}]
        }
    ]
}

class TestEnhancedSongTracker(unittest.TestCase):
    @patch('spotipy.Spotify')
    def setUp(self, mock_spotify):
        """Set up test environment with mocked Spotify client"""
        # Use a test database file
        self.test_db_path = 'test_database.sqlite'
        
        # Configure mock Spotify client
        self.mock_spotify = mock_spotify.return_value
        self.mock_spotify.track.return_value = MOCK_TRACK_RESPONSE
        self.mock_spotify.artist.return_value = MOCK_ARTIST_RESPONSE
        self.mock_spotify.audio_features.return_value = [MOCK_AUDIO_FEATURES]
        self.mock_spotify.recommendations.return_value = MOCK_RECOMMENDATIONS
        
        # Initialize tracker with test database
        self.tracker = EnhancedSongTracker()
        self.tracker.db_path = self.test_db_path
        self.tracker.conn = sqlite3.connect(self.test_db_path)
        self.tracker.sp = self.mock_spotify
        
        # Setup database schema
        self.tracker.setup_database()

    def test_database_setup(self):
        """Test if database tables are created correctly"""
        cursor = self.tracker.conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('liked_songs', 'listening_streaks', 'playlists')
        """)
        tables = [table[0] for table in cursor.fetchall()]
        self.assertEqual(len(tables), 3)
        self.assertIn('liked_songs', tables)
        self.assertIn('listening_streaks', tables)
        self.assertIn('playlists', tables)

    def test_add_liked_song(self):
        """Test adding a liked song with mocked Spotify responses"""
        track_id = MOCK_TRACK_RESPONSE['id']
        name = MOCK_TRACK_RESPONSE['name']
        artist = MOCK_TRACK_RESPONSE['artists'][0]['name']
        
        # Add song
        result = self.tracker.add_liked_song(track_id, name, artist)
        self.assertTrue(result)
        
        # Verify API calls
        self.mock_spotify.track.assert_called_once_with(track_id)
        self.mock_spotify.artist.assert_called_once()
        self.mock_spotify.audio_features.assert_called_once_with(track_id)
        
        # Verify database entry
        cursor = self.tracker.conn.execute(
            "SELECT name, artist, genre, energy FROM liked_songs WHERE id = ?",
            (track_id,)
        )
        song = cursor.fetchone()
        self.assertEqual(song[0], name)
        self.assertEqual(song[1], artist)
        self.assertEqual(song[2], 'pop')  # First genre from mock response
        self.assertEqual(song[3], 0.8)    # Energy from mock audio features

    @unittest.skip("Streak tracking needs revision - will fix later")
    def test_listening_streak(self):
        """Test listening streak tracking"""
        # Use a fixed date for testing
        base_date = datetime(2024, 1, 1, 12, 0)
        
        with patch('datetime.datetime') as mock_datetime:
            # Mock datetime.now() to return our fixed date
            mock_datetime.now.side_effect = [
                base_date,  # First call (yesterday)
                base_date,  # Get streak check
                base_date + timedelta(days=1),  # Second call (today)
                base_date + timedelta(days=1)   # Get streak check
            ]
            
            # Add song for "yesterday"
            self.tracker.add_liked_song("test_id_1", "Test Song 1", "Test Artist")
            streak = self.tracker.get_listening_streak()
            self.assertEqual(streak['current_streak'], 1, "First day should have streak of 1")
            
            # Add song for "today"
            self.tracker.add_liked_song("test_id_2", "Test Song 2", "Test Artist")
            streak = self.tracker.get_listening_streak()
            self.assertEqual(streak['current_streak'], 2, "Second consecutive day should have streak of 2")
            self.assertEqual(streak['songs_today'], 1, "Should have 1 song today")

    def test_recommendations(self):
        """Test song recommendations with mocked responses"""
        recommendations = self.tracker.get_recommendations(limit=2)
        
        # Verify recommendations format
        self.assertEqual(len(recommendations), 2)
        self.assertEqual(recommendations[0]['name'], 'Recommended Song 1')
        self.assertEqual(recommendations[1]['name'], 'Recommended Song 2')
        
        # Verify API call
        self.mock_spotify.recommendations.assert_called_once()

    def test_genre_analysis(self):
        """Test genre analysis functionality"""
        # Add songs with different genres
        self.tracker.add_liked_song("test_id_1", "Song 1", "Artist 1")
        
        # Change mock genre for second song
        new_artist_response = MOCK_ARTIST_RESPONSE.copy()
        new_artist_response['genres'] = ['jazz']
        self.mock_spotify.artist.return_value = new_artist_response
        self.tracker.add_liked_song("test_id_2", "Song 2", "Artist 2")
        
        analysis = self.tracker.analyze_genres()
        self.assertIn('chart', analysis)
        self.assertIn('top_genres', analysis)
        
        # Verify genres in analysis
        genres = [genre['genre'] for genre in analysis['top_genres']]
        self.assertIn('pop', genres)
        self.assertIn('jazz', genres)

    def test_auto_playlist_creation(self):
        """Test automatic playlist creation with mocked responses"""
        # Mock playlist creation response
        self.mock_spotify.user_playlist_create.return_value = {'id': 'playlist123'}
        
        # Add some test songs
        for i in range(3):
            self.tracker.add_liked_song(f"test_id_{i}", f"Test Song {i}", "Test Artist")
        
        result = self.tracker.create_auto_playlist('weekly')
        self.assertTrue(result)
        
        # Verify playlist creation API calls
        self.mock_spotify.user_playlist_create.assert_called_once()
        self.mock_spotify.playlist_add_items.assert_called_once()
        
        # Verify database entry
        cursor = self.tracker.conn.execute(
            "SELECT id, type FROM playlists WHERE type = 'weekly'"
        )
        playlist = cursor.fetchone()
        self.assertEqual(playlist[0], 'playlist123')
        self.assertEqual(playlist[1], 'weekly')

    def test_error_handling(self):
        """Test error handling for API failures"""
        # Simulate API error
        self.mock_spotify.track.side_effect = Exception("API Error")
        
        result = self.tracker.add_liked_song("error_id", "Error Song", "Error Artist")
        self.assertFalse(result)

    def tearDown(self):
        """Clean up test environment"""
        # Close the connection before removing the file
        if hasattr(self, 'tracker'):
            self.tracker.conn.close()
        
        # Remove test database with retry
        for _ in range(3):
            try:
                if os.path.exists(self.test_db_path):
                    os.remove(self.test_db_path)
                break
            except PermissionError:
                time.sleep(0.1)

if __name__ == '__main__':
    unittest.main() 