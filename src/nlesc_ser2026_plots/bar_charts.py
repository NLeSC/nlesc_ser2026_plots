"""Documentation about the nlesc_ser2026_plots module."""

import pandas as pd
import altair as alt
import plotly.graph_objects as go
from typing import Optional

from nlesc_ser2026_plots import my_nlesc_theme


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
    y_variable_right: Optional[str],
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

def create_survey_chart(
    df: pd.DataFrame,
    x_variable: str,
    x_variable_2: str,
    y_variable: Optional[str] = 'Question',
    dimensions: Optional[list[int]] = [700, 400],
    x_scale: Optional[alt.Scale] = 6,
) -> int:
    """Create a survey chart from a DataFrame.
    Args:
        df (pd.DataFrame): DataFrame with survey data.
        output_file (str): Path to save the output chart.
        dimensions (list[int], optional): Width and height of the chart. Defaults to [700, 400].
    Returns:
        int: Offset value for further processing.
    """

    alt.themes.enable("my_nlesc_theme")

    # Create the survey chart
    x_scale = alt.Scale(domain=[0, x_scale])
    chart = alt.Chart(df).mark_bar(size=40).encode(
        y=alt.Y(f'{y_variable}:N', sort='-y', title=None, 
                axis=alt.Axis(
                    labels=True, 
                    grid=False,
                    labelExpr="split(datum.label,'@')", 
                    labelLimit=350)),
        yOffset = alt.Column(f'{x_variable_2}:N', title=None),
        color=alt.Color(f'{x_variable_2}:N', title=["Evaluation"," period"], sort='descending'),
        opacity=alt.condition(
            alt.datum[x_variable_2] == '2013-2018', 
            alt.value(0.4),  # More transparent for 2013-2018
            alt.value(0.8)   # Fully opaque for other periods
        ),
        x=alt.X(f'{x_variable}:Q', 
                scale = x_scale, 
                axis=alt.Axis(
                    title=None, 
                    labels=True, 
                    grid=True,
                    gridColor='darkgray', 
                    tickCount=6, 
                    labelExpr="datum.value == 1 ? 'Strongly disagree' : datum.value == 2 ? 'Disagree' : datum.value == 3 ? 'Neutral' : datum.value == 4 ? 'Agree' : datum.value == 5 ? 'Strongly agree' : ''")),
    ).properties(
        width=dimensions[0],
        height=dimensions[1],
        title=alt.TitleParams(
            text='LA Survey Results'
        )
    )

    return chart

def create_pie_chart(
    df: pd.DataFrame,
    title: str,
    category_variable: str,
    value_variable: str,
    dimensions: Optional[list[int]] = [700, 400],
) -> alt.Chart:
    """Create a pie chart from a DataFrame.
        df (pd.DataFrame): DataFrame with categories and values.
    Args:
        title (str): Title for the chart.
        category_variable (str): Name of the column to use for categories.
        value_variable (str): Name of the column to use for values.
        dimensions (list[int], optional): Width and height of the chart. Defaults to [700, 400].
    Returns:
        alt.Chart: Altair chart object representing the pie chart.
    """

    alt.themes.enable("my_nlesc_theme")

    # Create the pie chart
    chart = alt.Chart(df).mark_arc().encode(
        theta=alt.Theta(f'{value_variable}:Q', stack=True),
        color=alt.Color(f'{category_variable}:N', 
                        sort='descending',
                        legend=alt.Legend(title=f'{category_variable}',
                                          labelExpr="split(datum.label,'@')", 
                                          orient='right', 
                                          titleAnchor='middle', 
                                          offset=-50)),
    ).properties(
        width=dimensions[0],
        height=dimensions[1],
        title=alt.TitleParams(
            text=title
        )
    )
    return chart

def create_sorted_bar_chart(
    df: pd.DataFrame,
    title: str,
    category_variable: str,
    value_variable: str,
    dimensions: Optional[list[int]] = [800, 400],
) -> alt.Chart:
    """Create a sorted bar chart from a DataFrame.
    Args:
        df (pd.DataFrame): DataFrame with categories and values.
        title (str): Title for the chart.
        category_variable (str): Name of the column to use for categories.
        value_variable (str): Name of the column to use for values.
        dimensions (list[int], optional): Width and height of the chart. Defaults to [700, 400].
    Returns:
        alt.Chart: Altair chart object representing the sorted bar chart.
    """

    alt.themes.enable("my_nlesc_theme")

    # Create the sorted bar chart
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X(f'{category_variable}:N', sort='-y', title=None, axis=alt.Axis(labelExpr="split(datum.label,'@')", labelAngle=45)),
        y=alt.Y(f'{value_variable}:Q', title=value_variable),
        color=alt.Color(f'Category:N', title=None)
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

def create_table_heatmap(
    df: pd.DataFrame,
    title: str,
    x_variable: str,
    y_variable: str,
    value_variable: str,
    x_range: Optional[list[int]] = None,
    dimensions: Optional[list[int]] = [500, 500],
) -> alt.Chart:
    """Create a table heatmap from a DataFrame.
    Args:
        df (pd.DataFrame): DataFrame with categories and values.
        title (str): Title for the chart.
        x_variable (str): Name of the column to use for x-axis.
        y_variable (str): Name of the column to use for y-axis.
        value_variable (str): Name of the column to use for values.
        dimensions (list[int], optional): Width and height of the chart. Defaults to [700, 400].
    Returns:
        alt.Chart: Altair chart object representing the table heatmap.
    """

    alt.themes.enable("my_nlesc_theme")

    x_range = [str(i) for i in range(*x_range)] if x_range else None

    base = alt.Chart(df).encode(
        x=alt.X(f'{x_variable}:O', title=None, scale=alt.Scale(domain=x_range, paddingInner=0) if x_range else None),
        y=alt.Y(f'{y_variable}:N', title=None, axis=alt.Axis(labelExpr="split(datum.label,'@')", labelLimit=350)),
    )

    # Create the table heatmap
    chart = base.mark_rect().encode(
        color=alt.Color(f'{value_variable}:Q', scale=alt.Scale(scheme='blues'), legend=None)
    )

    # Configure text
    text = base.transform_calculate(
        value=f'datum.{value_variable}/100'
    ).mark_text(baseline='middle', fontSize=20).encode(
        text=alt.Text('value:Q', format=".0%"), color=alt.value('white'), opacity=alt.condition(alt.datum.value > 0, alt.value(1), alt.value(0)))

    return (chart + text).properties(
        width=dimensions[0],
        height=dimensions[1],
        title=alt.TitleParams(
            text=title
        )
    )

def create_spiderweb_chart(
    df: pd.DataFrame,
    theta_variable: str,
    r_variable: str,
    category_variable: Optional[str] = None,
    title: Optional[str] = None,
    dimensions: Optional[list[int]] = [700, 700],
) -> alt.Chart:
    """Create a spiderweb (radar) chart from a DataFrame.
    Args:
        df (pd.DataFrame): DataFrame with categories and values.
        theta_variable (str): Name of the column to use for the angular axis.
        r_variable (str): Name of the column to use for the radial axis.
        dimensions (list[int], optional): Width and height of the chart. Defaults to [700, 400].
    Returns:
        alt.Chart: Altair chart object representing the spiderweb chart.
    """

    fig = go.Figure()
    for category in df[category_variable].unique() if category_variable else [None]:
        category_df = df[df[category_variable] == category] if category_variable else df
        category_df = pd.concat([category_df, category_df.iloc[[0]]], ignore_index=False)

        theme = my_nlesc_theme()['config']
        # Create the spiderweb chart
        fig.add_trace(go.Scatterpolar(
            r=category_df[r_variable],  # Add a small offset to ensure visibility
            theta=category_df[theta_variable],  # Add a small offset to ensure visibility
            fill='toself',
            name=category if category_variable else title,
        ))

    fig.update_layout(
        template=None,
        polar={
            'radialaxis': {
                'visible': True,
                'showticklabels': False,
                'ticks': '',
                'range': [0, df[r_variable].max() * 1.1]
            }
        },
        font_family=theme['axis']['titleFont'],
        font_size=theme['axis']['titleFontSize'],
        colorway=theme['range']['category'],
        font_color='black',
        font_weight='bold',
        showlegend=bool(category_variable),
        margin={'l': 40, 'r': 20, 't': 50, 'b': 40},
        legend={'yanchor': 'top', 'y': 0.9, 'xanchor': 'right', 'x': 1.0},
        title=title,
        title_x=0.
    )
    return fig

def save_radar_chart(
        chart: go.Figure, 
        output_file: str  
        ):
    """Save a radar chart as an HTML file.
    Args:
        chart (go.Figure): Plotly figure object representing the radar chart.
        output_file (str): Path to save the output HTML file.
    """
    import plotly.io as pio
    pio.write_html(chart, file=output_file, auto_open=False)