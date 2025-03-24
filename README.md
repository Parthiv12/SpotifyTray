# Spotify Song Tracker

A powerful Spotify integration that tracks your listening habits, creates personalized playlists, and provides detailed analytics through an interactive dashboard.

## Features

- 🎵 Track your liked songs and listening history
- 📊 Interactive dashboard with visualizations
- 🔥 Listening streak tracking
- 🎨 Genre analysis and distribution
- 🎯 Personalized song recommendations
- 📅 Automatic playlist creation (weekly/monthly)
- ⌨️ Customizable keyboard shortcuts
- 📈 Listening activity heatmap
- 🎼 Audio features analysis (energy, danceability, tempo)

## Prerequisites

- Python 3.8 or higher
- Spotify Premium account
- Spotify Developer credentials

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/spotify-song-tracker.git
cd spotify-song-tracker
```

2. Create and activate a virtual environment:
```bash
python -m venv .venv
.\.venv\Scripts\activate.bat  # On Windows
source .venv/bin/activate    # On Unix/MacOS
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up Spotify credentials:
   - Go to [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
   - Create a new application
   - Copy your Client ID and Client Secret
   - Create a `.env` file in the project root:
```
SPOTIFY_CLIENT_ID=your_client_id_here
SPOTIFY_CLIENT_SECRET=your_client_secret_here
SPOTIFY_REDIRECT_URI=http://localhost:8888/callback
```

## Usage

1. Start the application:
```bash
python src/main.py
```

2. Access the dashboard:
   - Open your browser and go to `http://localhost:8050`
   - Log in with your Spotify account when prompted

3. Configure keyboard shortcuts:
   - Edit `config/config.yaml` to customize your shortcuts
   - Default shortcuts:
     - Next track: Ctrl + Right
     - Previous track: Ctrl + Left
     - Like song: Ctrl + Up
     - Dislike song: Ctrl + Down

## Features in Detail

### Interactive Dashboard
- View your listening statistics
- Explore genre distribution
- Check your listening streak
- See personalized recommendations

### Automatic Playlists
- Weekly favorites playlist (created every Sunday)
- Monthly favorites playlist (created on the 1st of each month)
- Genre-based playlists

### Analytics
- Listening activity heatmap
- Genre distribution analysis
- Audio features visualization
- Listening streak tracking

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [Spotify API](https://developer.spotify.com/documentation/web-api/)
- [Dash](https://dash.plotly.com/)
- [Plotly](https://plotly.com/)
