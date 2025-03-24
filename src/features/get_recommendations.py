# src/features/get_recommendations.py
def get_recommendations(sp, limit: int = 2) -> list:
    """Get personalized song recommendations"""
    try:
        user_profile = sp.me()
        market = user_profile.get('country', 'US')
        top_tracks = sp.current_user_top_tracks(limit=2, time_range='short_term')
        seed_tracks = [track['id'] for track in top_tracks['items'] if track.get('id')] if top_tracks and top_tracks['items'] else []

        if len(seed_tracks) < 2:
            recent_tracks = sp.current_user_recently_played(limit=2)
            if recent_tracks and recent_tracks['items']:
                new_tracks = [item['track']['id'] for item in recent_tracks['items'] if item.get('track', {}).get('id') and item['track']['id'] not in seed_tracks]
                seed_tracks.extend(new_tracks[:2 - len(seed_tracks)])

        if not seed_tracks:
            print("No valid seed tracks found")
            return []

        # Log the full request URL
        request_url = f"https://api.spotify.com/v1/recommendations?seed_tracks={','.join(seed_tracks[:2])}&limit={limit}&market={market}"
        print(f"Requesting recommendations with URL: {request_url}")

        recommendations = sp.recommendations(
            seed_tracks=seed_tracks[:2],
            limit=limit,
            market=market
        )
        return [{
            'name': track['name'],
            'artist': track['artists'][0]['name'],
            'id': track['id']
        } for track in recommendations['tracks']] if recommendations and recommendations['tracks'] else []
    except Exception as e:
        print(f"Error getting recommendations: {e}")
        return []