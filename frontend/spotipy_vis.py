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

    def get_user_playlists(self, username):
        pls = self.sp.user_playlists(username)
        playlists = [
            {
                "Name": pl["name"],
                "Id": pl["id"],
                "Tracks": pl["tracks"]["total"],
                "Image": pl["images"][0]["url"] if pl["images"] else None,
            }
            for pl in pls["items"]
        ]
        return playlists

    def get_playlist_tracks(self, playlist_id):
        plts = self.sp.playlist_tracks(playlist_id)
        tracks = [
            {
                "Track": item["track"]["name"],
                "Id": item["track"]["id"],
                "Artist": ", ".join(
                    artist["name"] for artist in item["track"]["artists"]
                ),
                "Popularity": item["track"]["popularity"],
                "Duration (ms)": item["track"]["duration_ms"],
                # "Audio Features": afs[item["track"]["id"]],
            }
            for item in plts["items"]
        ]

        return pd.DataFrame(tracks)
