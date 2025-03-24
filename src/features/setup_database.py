# src/features/setup_database.py
import sqlite3
import os

def setup_database(db_path):
    """Setup enhanced database schema"""
    conn = sqlite3.connect(db_path)
    conn.executescript("""
        DROP TABLE IF EXISTS liked_songs;
        DROP TABLE IF EXISTS listening_streaks;
        DROP TABLE IF EXISTS playlists;

        CREATE TABLE liked_songs (
            id TEXT PRIMARY KEY,
            name TEXT,
            artist TEXT,
            genre TEXT DEFAULT 'Unknown',
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            energy FLOAT DEFAULT 0,
            danceability FLOAT DEFAULT 0,
            tempo FLOAT DEFAULT 0,
            acousticness FLOAT DEFAULT 0
        );

        CREATE TABLE listening_streaks (
            date DATE PRIMARY KEY,
            songs_played INTEGER DEFAULT 0,
            streak_count INTEGER DEFAULT 0
        );

        CREATE TABLE playlists (
            id TEXT PRIMARY KEY,
            name TEXT,
            type TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    return conn