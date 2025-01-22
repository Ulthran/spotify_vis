import boto3
import os
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotipyVis:
    def __init__(self, client_id=os.environ.get("SPOTIPY_CLIENT_ID"), credentials=None):
        if not credentials:
            print("Retrieving Spotipy credentials from SSM...")
            ssm = boto3.client("ssm")
            credentials_param = os.environ["CREDENTIALS_PARAM"]
            credentials_response = ssm.get_parameter(
                Name=credentials_param, WithDecryption=True
            )
            credentials = credentials_response["Parameter"]["Value"]
            print("Credentials retrieved from SSM!")

        self.auth_manager = SpotifyClientCredentials(
            client_id=client_id, client_secret=credentials
        )
        self.sp = spotipy.Spotify(auth_manager=self.auth_manager)

    def get_user(self, username):
        try:
            user = self.sp.user(username)
            return {
                "name": user["display_name"],
                "profile_url": user["external_urls"]["spotify"],
                "image_url": user["images"][0]["url"] if user["images"] else None,
                "followers": user["followers"]["total"],
            }
        except Exception:
            return {
                "name": "User Not Found",
                "profile_url": "#",
                "image_url": None,
                "followers": 0,
            }

    def get_monthlies(self):
        import re

        playlists = self.sp.user_playlists("charlie_bushman")
        monthlies = []
        while playlists:
            # Note that apparently some playlists' apostrophe is encoded as ' while others are ‘ so we search both with ['‘]
            playlists["items"] = [p for p in playlists["items"] if p]
            playlists["items"] = [
                p
                for p in playlists["items"]
                if re.search(r"[A-Z][a-z]{2} ['‘]\d{2}", p["name"])
            ]
            for playlist in playlists["items"]:
                playlist["name"] = playlist["name"].replace("‘", "'")
                monthlies.append(playlist)
            if playlists["next"]:
                playlists = self.sp.next(playlists)
            else:
                playlists = None

        return monthlies

    # Fetch Global Top Tracks
    def get_global_top_tracks(self):
        playlist_id = "37i9dQZF1DXcBWIGoYBM5M"  # Spotify's Top Today playlist
        results = self.sp.playlist_items(playlist_id, limit=10, market="US")
        tracks = [
            {
                "Track": item["track"]["name"],
                "Artist": ", ".join(
                    artist["name"] for artist in item["track"]["artists"]
                ),
                "Popularity": item["track"]["popularity"],
                "Duration (ms)": item["track"]["duration_ms"],
            }
            for item in results["items"]
        ]
        return pd.DataFrame(tracks)

    # Fetch Audio Features for a Track
    def get_audio_features(self, track_id):
        features = self.sp.audio_features([track_id])[0]
        return {
            "Danceability": features["danceability"],
            "Energy": features["energy"],
            "Tempo": features["tempo"],
            "Valence (Positivity)": features["valence"],
        }
