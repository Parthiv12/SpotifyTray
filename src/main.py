# src/main.py
from features.enhanced_song_tracker import EnhancedSongTracker

def main():
    tracker = EnhancedSongTracker()
    app = tracker.create_dashboard()  # Ensure this line is correct
    app.run(debug=True)

if __name__ == "__main__":
    main()