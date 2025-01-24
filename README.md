# spotify_vis
A serverless Spotify stats visualizer. Unfortunately Spotify recently removed public access for a lot of their fun stats so now we can pretty much only show popularity per song.

## Architecture

-  AWS SAM app with a Python 3.13 runtime
-  Uses Dash with Plotly for design and display
-  Uses Spotipy for Pythonic interaction with the Spotify Web API
-  Styled with Tailwind CSS (included through CDN)

## TODO

-  Include a proper test framework
  -  Maybe build it through AWS CodePipeline instead of GitHub Actions to get experience with that
-  Deploy production site to spotify.charliebushman.com