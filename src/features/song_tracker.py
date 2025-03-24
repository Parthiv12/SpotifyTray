import sqlite3
from datetime import datetime, timedelta
import os
import pandas as pd
import matplotlib.pyplot as plt

class SongTracker:
    def __init__(self):
        self.db_path = os.path.join('data', 'database.sqlite')
        os.makedirs('data', exist_ok=True)
        self.conn = sqlite3.connect(self.db_path)
        self.setup_database()

    def setup_database(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS liked_songs (
                id TEXT PRIMARY KEY,
                name TEXT,
                artist TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.conn.commit()

    def add_liked_song(self, track_id: str, name: str, artist: str):
        try:
            self.conn.execute("""
                INSERT OR REPLACE INTO liked_songs (id, name, artist)
                VALUES (?, ?, ?)
            """, (track_id, name, artist))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error adding song to database: {e}")
            return False

    def remove_liked_song(self, track_id: str):
        try:
            self.conn.execute("DELETE FROM liked_songs WHERE id = ?", (track_id,))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error removing song from database: {e}")
            return False

    def get_all_liked_songs(self):
        try:
            cursor = self.conn.execute("SELECT * FROM liked_songs")
            return cursor.fetchall()
        except Exception as e:
            print(f"Error fetching liked songs: {e}")
            return []

    def generate_report(self):
        df = pd.read_sql("SELECT * FROM liked_songs", self.conn)
        self.plot_genres(df)
        self.plot_activity(df)

    def plot_genres(self, df):
        plt.figure(figsize=(10, 6))
        df['artist'].value_counts().plot(kind='bar')
        plt.title('Favorite Artists')
        plt.savefig('artist_analysis.png')

    def generate_stats(self):
        try:
            # Create stats directory if it doesn't exist
            os.makedirs('data/stats', exist_ok=True)
            
            # Get data from last 30 days
            thirty_days_ago = datetime.now() - timedelta(days=30)
            df = pd.read_sql("""
                SELECT artist, COUNT(*) as count, 
                       strftime('%Y-%m-%d', timestamp) as date
                FROM liked_songs 
                WHERE timestamp > ?
                GROUP BY artist, date
                ORDER BY count DESC
            """, self.conn, params=(thirty_days_ago,))
            
            # Create figures directory
            stats_dir = 'data/stats'
            os.makedirs(stats_dir, exist_ok=True)
            
            # Generate artist popularity chart
            plt.figure(figsize=(12, 6))
            top_artists = df.groupby('artist')['count'].sum().sort_values(ascending=False).head(5)
            top_artists.plot(kind='bar')
            plt.title('Top Artists (Last 30 Days)')
            plt.xlabel('Artist')
            plt.ylabel('Songs Liked')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(stats_dir, 'top_artists.png'))
            plt.close()
            
            # Generate daily activity chart
            plt.figure(figsize=(12, 6))
            daily_likes = df.groupby('date')['count'].sum()
            daily_likes.plot(kind='line', marker='o')
            plt.title('Daily Liked Songs (Last 30 Days)')
            plt.xlabel('Date')
            plt.ylabel('Songs Liked')
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.savefig(os.path.join(stats_dir, 'daily_activity.png'))
            plt.close()
            
            return os.path.join(stats_dir, 'top_artists.png')
        except Exception as e:
            print(f"Error generating stats: {e}")
            return None 