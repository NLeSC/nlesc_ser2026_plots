import pandas as pd
import altair as alt
from typing import Optional

def create_yearly_multi_line_chart(
    df: pd.DataFrame,
    y_variable_left: str,
    y_variable_right: str,
    title: str,
    y_scale_left: Optional[list[int]],
    charge_year: Optional[str] = None,
    dimensions: Optional[list[int]] = [700, 400]):
        
    alt.themes.enable("my_nlesc_theme")

    year_col = df.index.name if df.index.name is not None else 'Year'

    # Create lines
    base = alt.Chart(df)

    line_left = base.mark_line(color='#009DDD', strokeWidth=3, point=alt.OverlayMarkDef(fill='#009DDD', size=100)).encode(
        x=alt.X(f'{year_col}:O'),
        y=alt.Y(f'{y_variable_left}:Q', title=y_variable_left, scale=alt.Scale(domain=y_scale_left)).axis(titleColor='#009DDD')
    )

    line_right = base.mark_line(color='#380339', strokeWidth=3, point=alt.OverlayMarkDef(fill='#380339', size=100)).encode(
        x=alt.X(f'{year_col}:O'),
        y=alt.Y(f'{y_variable_right}:Q', title=y_variable_right).axis(titleColor='#380339')
    )

    if charge_year is not None:
        ruler = alt.Chart(df).mark_rule(color='#FFB313', strokeDash=[8, 5], strokeWidth=5).encode(
            x=alt.X(f'{year_col}:O'),
            opacity=alt.condition(
                alt.datum[year_col] == charge_year,  # Replace 2023 with your desired year
                alt.value(0.8),
                alt.value(0.0)
            )
        )
        rect = alt.Chart(df).mark_rect(color='#FFB313').encode(
            x=alt.X(f'{year_col}:O'),
            x2=alt.value(dimensions[0]),
            opacity=alt.condition(
                alt.datum[year_col] == charge_year,  # Replace 2023 with your desired year
                alt.value(0.4),
                alt.value(0.0)
            )
        )
        chart = alt.layer(rect, ruler, line_left, line_right)
    else:
        chart = alt.layer(line_left, line_right)   

    chart = chart.resolve_scale(
        y='independent'
    ).resolve_axis(x = 'shared').properties(
        width=dimensions[0],
        height=dimensions[1],
        title=alt.TitleParams(
            text=title
        )
    )
    return chart
