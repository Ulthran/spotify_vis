from dash import callback, Dash, html, dcc, Input, Output, State
from datetime import date, datetime
import plotly.express as px
from spotipy_vis import SpotipyVis


def truncate_name(name: str, length: int = 20) -> str:
    return (name[:length] + "...") if len(name) > length else name


def build_app(dash_kwargs: dict = None) -> Dash:

    dash_kwargs = dash_kwargs or {}

    app = Dash(
        name=__name__,
        **dash_kwargs,
    )

    sv = SpotipyVis(
        client_id="1428584e1c294003bd962a4a441be19a",
        credentials="2e06b6708e924db293ea6396027303d3",
    )
    default_username = "charlie_bushman"
    default_user_info = sv.get_user(default_username)

    app.layout = html.Div(
        [
            # Meta
            html.Meta(
                name="ctbus Spotify Visualizer",
                content="Easily view trends in your music!",
            ),
            html.Title("ctbus Spotify Visualizer"),
            html.Link(
                rel="stylesheet",
                href="https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css",
                integrity="sha384-HtMZLkYo+pR5/u7zCzXxMJP6QoNnQJt1qkHM0EaOPvGDIzaVZbmYr/TlvUZ/sKAg",
                crossOrigin="anonymous",
            ),
            html.Div(
                className="bg-gray-100 text-gray-800 font-sans min-h-screen flex flex-col",
                children=[
                    # Header
                    html.Nav(
                        className="bg-gray-700 p-4 text-white",
                        children=[
                            html.Div(
                                className="container mx-auto flex justify-between",
                                children=[
                                    html.Div(
                                        className="flex items-center",
                                        children=[
                                            html.H1(
                                                "Spotify Visualizer", className="ml-2"
                                            ),
                                        ],
                                    ),
                                    html.Div(
                                        className="flex items-center",
                                        children=[
                                            html.A(
                                                "By ctbus",
                                                href="https://charliebushman.com",
                                                target="_blank",
                                                className="mr-2",
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    # Input for Username
                    html.Div(
                        className="container mx-auto flex flex-row items-center justify-center",
                        children=[
                            html.Label(
                                "Try your own username! -->",
                                htmlFor="username-input",
                                className="text-md m-4",
                            ),
                            dcc.Input(
                                id="username-input",
                                type="text",
                                placeholder="Enter Spotify Username",
                                value=default_username,
                                className="border border-gray-300 rounded p-2 m-4",
                            ),
                            html.Button(
                                "Submit",
                                id="submit-button",
                                n_clicks=0,
                                className="interest-button flex items-center bg-green-700 hover:bg-green-800 text-white text-lg font-bold font-mono py-2 px-4 rounded h-[40px] m-4",
                            ),
                        ],
                    ),
                    # Body
                    html.Div(
                        className="container flex flex-col lg:flex-row p-4 items-center justify-center",
                        children=[
                            # Hero Section
                            html.Div(
                                id="hero-section",
                                className="container text-center p-2",
                            ),
                            # Playlist Section
                            html.Div(
                                id="playlist-section",
                                className="container text-center p-2",
                                children=dcc.RadioItems(
                                    options=[],
                                    value="",
                                    id="playlists-selector",
                                ),
                            ),
                        ],
                    ),
                    # Main Plot
                    html.Div(
                        dcc.Graph(id="main-plot"),
                        className="container w-full p-2",
                    ),
                    # FAQs
                    html.Div(
                        [
                            html.Span(
                                "ℹ️",
                                className="text-blue-600 text-2xl cursor-pointer peer",
                            ),
                            html.Div(
                                "Spotify has been cracking down on access to their trainable data. We can no longer access audio features or analyses for tracks. :(",
                                className="text-sm text-gray-700 p-2 italic text-center",
                            ),
                        ],
                        className="container mx-auto md:w-1/2 flex flex-row justify-center items-center",
                    ),
                    html.Div(
                        [
                            html.Span(
                                "ℹ️",
                                className="text-blue-600 text-2xl cursor-pointer peer",
                            ),
                            html.Div(
                                "It can be tricky to find your Spotify username (NOT YOUR DISPLAY NAME). Try going to https://open.spotify.com, click on your profile (top right) and then select Profile. The URL should then be something like https://open.spotify.com/user/your_username where 'your_username' is what you can submit here to see your public playlist stats.",
                                className="text-sm text-gray-700 p-2 italic text-center",
                            ),
                        ],
                        className="container mx-auto md:w-1/2 flex flex-row justify-center items-center",
                    ),
                    html.Div(
                        [
                            html.Span(
                                "ℹ️",
                                className="text-blue-600 text-2xl cursor-pointer peer",
                            ),
                            html.Div(
                                "Entering your Spotify username will only show you publicly available data. You aren't logging into your account, sharing any private information, or giving any third party access.",
                                className="text-sm text-gray-700 p-2 italic text-center",
                            ),
                        ],
                        className="container mx-auto md:w-1/2 flex flex-row justify-center items-center",
                    ),
                    # Footer
                    html.Div(className="flex-grow"),
                    html.Footer(
                        className="bg-gray-300 text-gray-700 text-center py-2",
                        children=[
                            html.Div(
                                className="container mx-auto",
                                children=[
                                    html.P(
                                        "© 2025 Charlie Bushman. All rights reserved."
                                    )
                                ],
                            )
                        ],
                    ),
                ],
            ),
        ]
    )

    # Callback to Update Hero Section
    @app.callback(
        Output("hero-section", "children"),
        Input("submit-button", "n_clicks"),
        State("username-input", "value"),
    )
    def update_hero_section(n_clicks, username):
        # Fetch user info
        user_info = sv.get_user(username)
        # Create hero section content
        return html.A(
            href=user_info["profile_url"],
            target="_blank",
            children=[
                html.Div(
                    className="container flex flex-row border border-black rounded-full max-w-xl overflow-hidden",
                    children=[
                        (
                            html.Img(
                                src=user_info["image_url"],
                                className="w-36 h-36 rounded-full",
                            )
                            if user_info["image_url"]
                            else None
                        ),
                        html.Div(
                            className="flex flex-col justify-center ml-4 overflow-x-auto",
                            children=[
                                html.H1(
                                    user_info["name"],
                                    className="text-4xl font-bold mb-2",
                                ),
                                html.P(
                                    f"Followers: {user_info['followers']}",
                                    className="text-lg",
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )

    @app.callback(
        Output("playlist-section", "children"),
        Input("submit-button", "n_clicks"),
        State("username-input", "value"),
    )
    def update_playlist_section(n_clicks, username):
        # Fetch user playlists
        user_playlists = sv.get_user_playlists(username)
        # Create playlist section content
        return html.Div(
            className="container flex flex-row mx-auto p-4 max-w-2xl",
            children=[
                dcc.RadioItems(
                    className="flex flex-wrap max-h-48 overflow-y-scroll border border-black rounded-lg justify-space-between",
                    options=[
                        {
                            "label": html.Div(
                                children=[
                                    html.Img(
                                        src=pl["Image"],
                                        className=" min-w-24 w-24 h-24 rounded-lg m-2 p-1",
                                    ),
                                    html.P(
                                        truncate_name(f"{pl['Name']}"),
                                        className="text-sm w-24 p-1",
                                    ),
                                ],
                                className="flex flex-col items-center",
                            ),
                            "value": pl["Id"],
                        }
                        for pl in user_playlists
                    ],
                    value=user_playlists[0]["Id"],
                    inline=True,
                    id="playlists-selector",
                ),
            ],
        )

    @app.callback(
        Output("main-plot", "figure"),
        Input("playlists-selector", "value"),
        State("playlists-selector", "value"),
    )
    def update_plot(selected_playlist_id, selected_playlist_name):
        # Create a bar plot for the selected feature
        fig = px.bar(
            sv.get_playlist_tracks(selected_playlist_id),
            x="Track",
            y="Popularity",
            title=f"{'Popularity'.capitalize()} for Songs in Playlist",
            labels={"Track": "Track Name", "Popularity": "Popularity".capitalize()},
            template="plotly_dark",
        )
        fig.update_layout(xaxis_tickangle=-45, height=600, margin={"t": 50, "b": 150})
        return fig

    return app


if __name__ == "__main__":
    build_app().run(debug=True)
