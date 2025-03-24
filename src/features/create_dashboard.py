# src/features/create_dashboard.py
from dash import Dash, html, dcc, Output, Input
import dash_bootstrap_components as dbc
from .analyze_genres import analyze_genres
from .generate_heatmap import generate_heatmap
from .get_recommendations import get_recommendations

def create_dashboard(sp, conn):
    """Create interactive dashboard"""
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    app.layout = dbc.Container([
        html.H1('Spotify Song Tracker Dashboard'),

        dbc.Row([
            dbc.Col([
                html.H3('Genre Analysis'),
                dcc.Graph(id='genre-chart')
            ]),
            dbc.Col([
                html.H3('Recommended Songs'),
                html.Div(id='recommendations')
            ])
        ]),

        dbc.Row([
            dbc.Col([
                html.H3('Listening Activity Heatmap'),
                dcc.Graph(id='heatmap')
            ])
        ]),

        dcc.Interval(
            id='interval-component',
            interval=30*1000,  # 30 seconds
            n_intervals=0
        )
    ])

    @app.callback(
        [Output('genre-chart', 'figure'),
         Output('heatmap', 'figure'),
         Output('recommendations', 'children')],
        Input('interval-component', 'n_intervals')
    )
    def update_dashboard(n):
        try:
            genres = analyze_genres(conn)
            heatmap = generate_heatmap(conn)
            recommendations = get_recommendations(sp)

            recommendations_html = html.Ul([
                html.Li(f"{rec['name']} - {rec['artist']}")
                for rec in recommendations
            ])

            return genres['chart'], heatmap, recommendations_html
        except Exception as e:
            print(f"Dashboard update error: {e}")
            return {}, {}, html.Div("No data available")

    return app  # Return the app instead of running it