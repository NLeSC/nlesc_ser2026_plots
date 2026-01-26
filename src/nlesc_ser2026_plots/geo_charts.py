import altair as alt
import geopandas as gpd
import pandas as pd
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon

def plot_netherlands_with_institutions(data: pd.DataFrame):
    """
    Plots the Netherlands as a grey-filled shape with dots representing institutions.

    Parameters:
    - data (pd.DataFrame): A DataFrame with columns ['institution', 'latitude', 'longitude'].

    Returns:
    - alt.Chart: An Altair chart object.
    """
    # Load Netherlands shapefile using GeoPandas
    netherlands = gpd.read_file('https://raw.githubusercontent.com/datasets/geo-countries/master/data/countries.geojson')
    netherlands = netherlands[netherlands['name'] == 'Netherlands']

    projection_args = {
        'type': 'mercator',
        'scale': 6000,
        'center': [5.3, 52.1]
    }
    # Create a base map of the Netherlands
    netherlands_chart = alt.Chart(netherlands).mark_geoshape(
        fill='lightgrey',
        stroke='white'
    ).project(
        **projection_args
    ).properties(
        width=600,
        height=800
    )

    # Create a points layer for the institutions

    points_chart = alt.Chart(data).project(
        **projection_args
    ).mark_circle(size=50, color='#009DDD').encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        tooltip=['institution:N']
    )
    # Define a fixed location in Amsterdam
    amsterdam_location = {'longitude': 4.895168, 'latitude': 52.370216}

    def generate_bezier_points(p0, p1, control, num_points=100):
        """
        Generate points for a quadratic Bezier curve.

        Parameters:
        - p0: Start point (longitude, latitude).
        - p1: End point (longitude, latitude).
        - control: Control point (longitude, latitude).
        - num_points: Number of points to generate along the curve.

        Returns:
        - A list of points (longitude, latitude) along the curve.
        """
        t_values = np.linspace(0, 1, num_points)
        bezier_points = [
            (
                (1 - t)**2 * p0[0] + 2 * (1 - t) * t * control[0] + t**2 * p1[0],
                (1 - t)**2 * p0[1] + 2 * (1 - t) * t * control[1] + t**2 * p1[1]
            )
            for t in t_values
        ]
        return bezier_points

    curves_data = []
    for _, row in data.iterrows():
        start = (row['longitude'], row['latitude'])
        end = (amsterdam_location['longitude'], amsterdam_location['latitude'])
        control = ((start[0] + end[0]) / 2, max(start[1], end[1]) + 0.1)  # Control point above the midpoint
        bezier_points = generate_bezier_points(start, end, control)
        curves_data.extend([
            {'longitude': point[0], 'latitude': point[1], 'institution': row['institution']}
            for point in bezier_points
        ])

    curves_data = pd.DataFrame(curves_data)

    # Create a curved splines layer
    curves_chart = alt.Chart(curves_data).project(
        **projection_args
    ).mark_line(color='#380339', opacity=0.6).encode(
        longitude='longitude:Q',
        latitude='latitude:Q',
        detail='institution:N'
    )

    # Combine the points and curves layers
    return netherlands_chart + points_chart + curves_chart
