# src/features/generate_heatmap.py
import pandas as pd
import plotly.graph_objects as go

def generate_heatmap(conn) -> go.Figure:
    """Generate listening activity heatmap"""
    df = pd.read_sql("""
        SELECT 
            strftime('%H', timestamp) as hour,
            strftime('%w', timestamp) as day,
            COUNT(*) as count
        FROM liked_songs
        GROUP BY hour, day
    """, conn)

    fig = go.Figure(data=go.Heatmap(
        z=df.pivot(index='day', columns='hour', values='count').values,
        x=df['hour'].unique(),
        y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    ))

    fig.update_layout(
        title='Listening Activity Heatmap',
        xaxis_title='Hour of Day',
        yaxis_title='Day of Week'
    )

    return fig