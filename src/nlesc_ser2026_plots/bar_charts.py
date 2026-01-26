"""Documentation about the nlesc_ser2026_plots module."""

import pandas as pd
import altair as alt
from typing import Optional


def create_yearly_stacked_bar_chart(
    df: pd.DataFrame,
    y_variable: str,
    color_variable: str,
    title: str,
    dimensions: Optional[list[int]] = [700, 400],
) -> alt.Chart:
    """Create a yearly stacked bar chart from a DataFrame.
    Args:
        df (pd.DataFrame): DataFrame with years as index and categories as columns.
        y_variable (str): Name of the column to use for the y-axis values.
        color_variable (str): Name of the column to use for the color encoding.
        title (str): Title for the chart.
        dimensions (list[int], optional): Width and height of the chart. Defaults to [700, 400].
    Returns:
        alt.Chart: Altair chart object representing the stacked bar chart.
    """

    alt.themes.enable("my_nlesc_theme")

    year_col = df.index.name if df.index.name is not None else 'Year'
    
    # Create the stacked bar chart
    chart = alt.Chart(df).transform_joinaggregate(
        order=f'sum({y_variable})',
        groupby=[f'{color_variable}']
    ).mark_bar().encode(
        x=alt.X(f'{year_col}:O', title='Year'),
        y=alt.Y(f'{y_variable}:Q', axis=alt.Axis(title=y_variable, labels=True, grid=True)),
        color=alt.Color(f'{color_variable}:N', sort=alt.SortField(field='order', order='descending')).legend(title=color_variable,labelExpr="split(datum.label,'@')"),
        order=alt.Order('order:Q', sort='descending')  # Ensure proper stacking order
    ).properties(
        width=dimensions[0],
        height=dimensions[1],
        title=alt.TitleParams(
            text=title
        )
    ).resolve_scale(
        color='independent'
    )
    return chart



def create_yearly_bar_line_chart(
    df: pd.DataFrame,
    title: str,
    y_variable_left: str,
    y_variable_right: str,
    dimensions: Optional[list[int]] = [700, 400],
) -> alt.Chart:
    """Create a bar and line chart showing submissions and acceptance rate over years.
    """
    
    year_col = df.index.name if df.index.name is not None else 'Year'

    alt.themes.enable("my_nlesc_theme")
    # Create bar chart for Submissions
    bar = alt.Chart(df).mark_bar(color='#009DDD').encode(
        x=alt.X(f'{year_col}:O'),
        y=alt.Y(f'{y_variable_left}:Q', title=y_variable_left).axis(titleColor='#009DDD')
    )
    # Create line chart for Acceptance Rate
    line = alt.Chart(df).mark_line(color='#380339', strokeWidth=3).encode(
        x=alt.X(f'{year_col}:O'),
        y=alt.Y(f'{y_variable_right}:Q', title=y_variable_right, scale=alt.Scale(domain=[0, 100])).axis(titleColor='#380339')
    )

    # Combine bar and line charts with dual y-axes
    chart = alt.layer(bar, line).resolve_scale(
        y='independent'
    ).properties(
        width=dimensions[0],
        height=dimensions[1],
        title=alt.TitleParams(
            text=title
        )
    )
    return chart


def create_yearly_stacked_bar_line_chart(
    df: pd.DataFrame,
    title: Optional[str],
    y_variable_left: str,
    y_variable_right: str,
    color_variable: str,
    dimensions: Optional[list[int]] = [700, 400],
) -> alt.Chart:
    """Create a bar and line chart showing submissions and acceptance rate over years.
    """
    
    year_col = df.index.name if df.index.name is not None else 'Year'

    alt.themes.enable("my_nlesc_theme")
    # Create bar chart for Submissions
    bar = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{year_col}:O'),
        y=alt.Y(f'{y_variable_left}:Q', title=y_variable_left),
        color=alt.Color(f'{color_variable}:N', sort=alt.SortField(field=f'sum({y_variable_left})', order='descending')).legend(title=color_variable,labelExpr="split(datum.label,'@')"),
        order=alt.Order(f'sum{y_variable_left}:Q', sort='descending')  # Ensure proper stacking order
    )
    # Create line chart for Acceptance Rate
    line = alt.Chart(df).mark_line(color='#380339', strokeWidth=3).encode(
        x=alt.X(f'{year_col}:O'),
        y=alt.Y(f'{y_variable_right}:Q', title=y_variable_right, scale=alt.Scale(domain=[0, 100])).axis(titleColor='#380339')
    )

    # Combine bar and line charts with dual y-axes
    chart = alt.layer(bar, line).resolve_scale(
        y='independent'
    ).properties(
        width=dimensions[0],
        height=dimensions[1],
        title=alt.TitleParams(
            text=title
        )
    )
    return chart



def create_yearly_multi_bar_chart(
    df: pd.DataFrame,
    title: str,
    y_variable: str,
    offset_variable: str,
    dimensions: Optional[list[int]] = [700, 400],
) -> alt.Chart:
    """Create a multi-bar chart over years    """

    year_col = df.index.name if df.index.name is not None else 'Year'

    alt.themes.enable("my_nlesc_theme")

    # Create the grouped bar chart
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{year_col}:O'),
        y=alt.Y(y_variable, title=y_variable),
        color=alt.Color(f'{offset_variable}:N', title=None),
        xOffset=alt.Column(f'{offset_variable}:N', title=None)
    ).properties(
        width=dimensions[0],  # Adjust width for grouped bars
        height=dimensions[1],
        title=alt.TitleParams(
            text=title
        )
    )
    return chart


