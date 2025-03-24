# Spotify Liker

A simple Windows application that lets you like/unlike Spotify songs with keyboard shortcuts.

## Features
- Like/Unlike currently playing songs with keyboard shortcuts
- System tray icon for easy access
- Windows notifications
- Track your liked songs history

## Requirements
- Python 3.8+
- Spotify Premium account
- Windows OS

## Installation
1. Clone this repository
2. Create a `.env` file from `.env.example`
3. Add your Spotify API credentials to `.env`
4. Run `pip install -r requirements.txt`
5. Double-click `run_spotify_liker.bat` to start

## Usage
- Press `Ctrl+Alt+7` to like the current song
- Press `Ctrl+Alt+8` to unlike the current song
- Check system tray for icon and options
- Notifications will show when songs are liked/unliked

## Spotify API Setup
1. Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new application
3. Add `http://localhost:8888/callback` to Redirect URIs
4. Copy Client ID and Client Secret to `.env` file

## Contributing
Feel free to open issues or submit pull requests!
