"""Documentation about the nlesc_ser2026_plots module."""

import pandas as pd
import altair as alt
from typing import Optional


def create_stacked_bar_chart(
    df: pd.DataFrame,
    title: Optional[str] = "FTE Allocation by Activity per Year",
    width: int = 600,
    height: int = 400
) -> alt.Chart:
    """Create a stacked bar chart showing FTE allocation by activity per year.

    Function creates a stacked bar chart from a dataframe where rows represent
    calendar years and columns represent different activities, with values
    being the number of FTE spent on each activity.

    Args:
        df (pd.DataFrame): DataFrame with years as index and activities as columns.
                          Values should be FTE numbers.
        title (str, optional): Title for the chart. Defaults to
                             "FTE Allocation by Activity per Year".
        width (int): Width of the chart in pixels. Defaults to 600.
        height (int): Height of the chart in pixels. Defaults to 400.

    Returns:
        alt.Chart: Altair chart object representing the stacked bar chart.

    Raises:
        ValueError: If the dataframe is empty or has no numeric columns.
        TypeError: If df is not a pandas DataFrame.

    Example:
        Create a stacked bar chart from FTE data:

        >>> import pandas as pd
        >>> data = {
        ...     'Research Projects': [2.5, 3.0, 2.8],
        ...     'Trainings': [1.0, 1.2, 1.5],
        ...     'Community Building': [0.5, 0.8, 0.7]
        ... }
        >>> df = pd.DataFrame(data, index=[2021, 2022, 2023])
        >>> chart = create_stacked_bar_chart(df)
        >>> chart.show()  # Display the chart
    """
    if not isinstance(df, pd.DataFrame):
        msg = "Input must be a pandas DataFrame"
        raise TypeError(msg)
    
    if df.empty:
        msg = "DataFrame cannot be empty"
        raise ValueError(msg)
    
    # Check if there are numeric columns
    numeric_cols = df.select_dtypes(include=['number']).columns
    if len(numeric_cols) == 0:
        msg = "DataFrame must contain at least one numeric column"
        raise ValueError(msg)
    
    # Prepare data for Altair (melt to long format)
    # Reset index to make year a column if it's currently the index
    if df.index.name is None:
        df.index.name = 'Year'
    
    df_reset = df.reset_index()
    year_col = df_reset.columns[0]
    
    # Melt the dataframe to long format
    df_melted = df_reset.melt(
        id_vars=[year_col],
        var_name='Activity',
        value_name='FTE'
    )
    
    # Create the stacked bar chart
    chart = alt.Chart(df_melted).mark_bar().encode(
        x=alt.X(f'{year_col}:O', title='Year', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('FTE:Q', title='Full-Time Equivalent (FTE)'),
        color=alt.Color(
            'Activity:N',
            title='Activity',
            scale=alt.Scale(scheme='category20')
        ),
        tooltip=[
            alt.Tooltip(f'{year_col}:O', title='Year'),
            alt.Tooltip('Activity:N', title='Activity'),
            alt.Tooltip('FTE:Q', title='FTE', format='.2f')
        ]
    ).properties(
        width=width,
        height=height,
        title=alt.TitleParams(
            text=title,
            fontSize=16,
            anchor='start'
        )
    ).resolve_scale(
        color='independent'
    )
    
    return chart
