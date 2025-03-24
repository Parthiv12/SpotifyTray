import yaml
import os
from typing import Dict, Any

class Config:
    def __init__(self):
        self.config_path = 'config.yaml'
        self.load_config()
    
    def load_config(self):
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                self.settings = yaml.safe_load(f)
        else:
            self.settings = self.default_settings()
            self.save_config()
    
    def save_config(self):
        with open(self.config_path, 'w') as f:
            yaml.dump(self.settings, f)
    
    def default_settings(self) -> Dict[str, Any]:
        return {
            'hotkeys': {
                'like_song': 'ctrl+alt+7',
                'unlike_song': 'ctrl+alt+8'
            },
            'notifications': {
                'duration': 'long'
            }
        }
    
    def get_hotkey(self, action: str) -> str:
        return self.settings['hotkeys'].get(action, '') 