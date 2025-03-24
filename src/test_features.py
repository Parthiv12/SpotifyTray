import unittest
from features.enhanced_song_tracker import EnhancedSongTracker
import os
from datetime import datetime, timedelta

class TestEnhancedSongTracker(unittest.TestCase):
    def setUp(self):
        """Set up test environment"""
        self.tracker = EnhancedSongTracker()
        
    def test_database_setup(self):
        """Test if database tables are created correctly"""
        cursor = self.tracker.conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name IN ('liked_songs', 'listening_streaks', 'playlists')
        """)
        tables = cursor.fetchall()
        self.assertEqual(len(tables), 3)
        
    def test_add_liked_song(self):
        """Test adding a liked song"""
        # Test with a sample Spotify track ID
        track_id = "11dFghVXANMlKmJXsNCbNl"  # Sample track ID
        name = "Test Song"
        artist = "Test Artist"
        
        result = self.tracker.add_liked_song(track_id, name, artist)
        self.assertTrue(result)
        
        # Verify song was added to database
        cursor = self.tracker.conn.execute(
            "SELECT * FROM liked_songs WHERE id = ?",
            (track_id,)
        )
        song = cursor.fetchone()
        self.assertIsNotNone(song)
        self.assertEqual(song[1], name)
        self.assertEqual(song[2], artist)
        
    def test_listening_streak(self):
        """Test listening streak functionality"""
        # Add a song to trigger streak update
        self.tracker.add_liked_song("test_id", "Test Song", "Test Artist")
        
        # Get streak info
        streak = self.tracker.get_listening_streak()
        self.assertIsInstance(streak, dict)
        self.assertIn('current_streak', streak)
        self.assertIn('songs_today', streak)
        
    def test_genre_analysis(self):
        """Test genre analysis functionality"""
        # Add a test song with a genre
        self.tracker.add_liked_song("test_id", "Test Song", "Test Artist")
        
        # Get genre analysis
        analysis = self.tracker.analyze_genres()
        self.assertIsInstance(analysis, dict)
        self.assertIn('chart', analysis)
        self.assertIn('top_genres', analysis)
        
    def test_recommendations(self):
        """Test song recommendations"""
        recommendations = self.tracker.get_recommendations(limit=3)
        self.assertIsInstance(recommendations, list)
        self.assertLessEqual(len(recommendations), 3)
        
    def test_auto_playlist(self):
        """Test automatic playlist creation"""
        # Add some test songs
        for i in range(3):
            self.tracker.add_liked_song(
                f"test_id_{i}",
                f"Test Song {i}",
                f"Test Artist {i}"
            )
        
        # Test weekly playlist creation
        result = self.tracker.create_auto_playlist('weekly')
        self.assertTrue(result)
        
        # Verify playlist was created in database
        cursor = self.tracker.conn.execute(
            "SELECT * FROM playlists WHERE type = 'weekly'"
        )
        playlist = cursor.fetchone()
        self.assertIsNotNone(playlist)
        
    def tearDown(self):
        """Clean up test environment"""
        # Close database connection
        self.tracker.conn.close()

if __name__ == '__main__':
    unittest.main() 