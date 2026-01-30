"""Documentation about nlesc_ser2026_plots."""

import logging
import altair as alt
from pyalex import config

logging.getLogger(__name__).addHandler(logging.NullHandler())

__author__ = "Gijs van den Oord"
__email__ = "g.vandenoord@esciencecenter.nl"
__version__ = "0.1.0"

config.email = __email__
config.max_retries = 10
config.retry_backoff_factor = 0.1
config.retry_http_codes = [429, 500, 503]

# Define a dictionary to hold all style elements
def my_nlesc_theme():
    """Custom NLESC theme for Altair charts."""
    return {
        "config": {
            "title": {
                "fontSize": 30,
                "anchor": "start",
                "font": "Nunito",
            },
            "axis": {
                "labelFont": "Calibri",
                "labelFontSize": 20,
                "titleFont": "Nunito",
                "titleFontSize": 26,
            },
            "legend": {
                "labelFont": "Calibri",
                "labelFontSize": 20,
                "titleFont": "Nunito",
                "titleFontSize": 24,
            },
            "axisX": {
                "labelAngle": 0,
            },
            "range": {"category": ["#009DDD", "#380339", "#FFB313",  "#016004", "#0808C6", "#6A4C93"]},
            "facet_cell": {
                "strokeWidth": 1
            },
            "bar": {
                "stroke": "white",
                "strokeWidth": 2,
                "opacity": 0.75
            }
        }
    }

# Register the custom theme
alt.themes.register("my_nlesc_theme", my_nlesc_theme)
