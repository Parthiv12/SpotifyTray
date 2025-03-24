# src/features/check_access_token.py
def check_access_token(sp):
    """Check if the access token is valid"""
    try:
        user_profile = sp.me()  # This will raise an error if the token is invalid
        print("Access token is valid. User profile:", user_profile)
    except Exception as e:
        print(f"Access token is invalid: {e}")