spotify_liker/
│
├── src/
│   ├── __init__.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── spotify_client.py      # Spotify API handling
│   │   ├── notification.py        # Notification system
│   │   └── hotkeys.py            # Keyboard shortcuts
│   │
│   ├── features/
│   │   ├── __init__.py
│   │   ├── song_tracker.py       # Listening habits
│   │   ├── recommendations.py    # Smart recommendations
│   │   └── playlist_manager.py   # Playlist operations
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── database.py          # SQLite handling
│   │   └── config.py            # Configuration management
│   │
│   └── ui/
│       ├── __init__.py
│       └── tray_icon.py         # System tray interface
│
├── data/
│   └── database.sqlite          # SQLite database
│
├── config/
│   ├── config.yaml             # User configuration
│   └── .env.example            # Environment template
│
├── scripts/
│   ├── install.bat             # Installation script
│   └── run.bat                 # Startup script
│
├── tests/
│   └── test_core.py            # Unit tests
│
├── requirements.txt            # Dependencies
├── README.md                   # Documentation
└── main.py                     # Entry point
