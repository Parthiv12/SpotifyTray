# src/features/analyze_genres.py
import pandas as pd
import plotly.express as px

def analyze_genres(conn) -> dict:
    """Analyze genre distribution"""
    df = pd.read_sql("""
        SELECT genre, COUNT(*) as count
        FROM liked_songs
        GROUP BY genre
        ORDER BY count DESC
    """, conn)

    fig = px.pie(
        df,
        values='count',
        names='genre',
        title='Genre Distribution'
    )

    return {
        'chart': fig,
        'top_genres': df.head(5).to_dict('records')
    }