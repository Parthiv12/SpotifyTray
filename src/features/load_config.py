import os
import yaml

def load_config():
    """Load configuration including custom shortcuts"""
    config_path = os.path.join('config', 'config.yaml')
    os.makedirs('config', exist_ok=True)
    if os.path.exists(config_path):
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    else:
        config = {
            'shortcuts': {
                'next_track': 'ctrl+right',
                'previous_track': 'ctrl+left',
                'like_song': 'ctrl+up',
                'dislike_song': 'ctrl+down'
            },
            'playlist_settings': {
                'weekly_playlist_name': 'Weekly Favorites',
                'monthly_playlist_name': 'Monthly Favorites',
                'genre_playlist_prefix': 'Genre: '
            }
        }
        with open(config_path, 'w') as f:
            yaml.dump(config, f)
        return config
