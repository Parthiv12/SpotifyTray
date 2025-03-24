# src/features/setup_keyboard_shortcuts.py
import keyboard
import winotify

def setup_keyboard_shortcuts(sp, add_liked_song, remove_liked_song, config):
    """Setup keyboard shortcuts"""
    def on_next_track():
        keyboard.send('next track')

    def on_previous_track():
        keyboard.send('previous track')

    def on_like_song():
        current_track = sp.current_playback()
        if current_track and current_track['item']:
            track = current_track['item']
            add_liked_song(
                track['id'],
                track['name'],
                track['artists'][0]['name']
            )
            notification = winotify.Notification(
                app_id="Spotify Tracker",
                title="Song Liked",
                msg=f"Added {track['name']} to your liked songs!"
            )
            notification.show()

    def on_dislike_song():
        current_track = sp.current_playback()
        if current_track and current_track['item']:
            track = current_track['item']
            remove_liked_song(track['id'])
            notification = winotify.Notification(
                app_id="Spotify Tracker",
                title="Song Removed",
                msg=f"Removed {track['name']} from your liked songs!"
            )
            notification.show()

    # Load shortcuts from config
    shortcuts = config.get('shortcuts', {
        'next_track': 'ctrl+right',
        'previous_track': 'ctrl+left',
        'like_song': 'ctrl+up',
        'dislike_song': 'ctrl+down'
    })

    # Register keyboard shortcuts
    keyboard.add_hotkey(shortcuts['next_track'], on_next_track)
    keyboard.add_hotkey(shortcuts['previous_track'], on_previous_track)
    keyboard.add_hotkey(shortcuts['like_song'], on_like_song)
    keyboard.add_hotkey(shortcuts['dislike_song'], on_dislike_song)