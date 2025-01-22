from dash import callback, Dash, html, dcc, Input, Output, State
from datetime import date, datetime
from spotipy_vis import SpotipyVis


def build_app(dash_kwargs: dict = None) -> Dash:

    dash_kwargs = dash_kwargs or {}

    app = Dash(
        name=__name__,
        **dash_kwargs,
    )

    sv = SpotipyVis()
    default_username = "charlie_bushman"
    default_user_info = sv.get_user(default_username)

    app.layout = html.Div(
        [
            # Input for Username
            html.Div(
                [
                    dcc.Input(
                        id="username-input",
                        type="text",
                        placeholder="Enter Spotify Username",
                        value=default_username,
                        style={
                            "marginRight": "10px",
                            "padding": "5px",
                            "width": "300px",
                        },
                    ),
                    html.Button(
                        "Submit",
                        id="submit-button",
                        n_clicks=0,
                        style={"padding": "5px 10px"},
                    ),
                ],
                style={"textAlign": "center", "marginTop": "20px"},
            ),
            # Hero Section
            html.Div(
                id="hero-section",
                style={
                    "textAlign": "center",
                    "padding": "50px",
                    "backgroundColor": "#f5f5f5",
                    "borderBottom": "2px solid #ddd",
                },
            ),
            # Placeholder for Additional Sections
            html.Div(
                [
                    html.H2("Other Content Goes Here"),
                    html.P(
                        "You can add additional content or sections below the hero section."
                    ),
                ]
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
        return html.Div(
            [
                (
                    html.Img(
                        src=user_info["image_url"],
                        style={
                            "width": "150px",
                            "height": "150px",
                            "borderRadius": "50%",
                        },
                    )
                    if user_info["image_url"]
                    else None
                ),
                html.H1(
                    user_info["name"],
                    style={"textAlign": "center", "marginTop": "20px"},
                ),
                html.A(
                    "Visit Profile",
                    href=user_info["profile_url"],
                    target="_blank",
                    style={
                        "display": "block",
                        "textAlign": "center",
                        "marginTop": "10px",
                        "textDecoration": "none",
                        "color": "blue",
                    },
                ),
            ]
        )

    return app


if __name__ == "__main__":
    build_app().run(debug=True)
