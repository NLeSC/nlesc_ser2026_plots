#!/usr/bin/env python3

import pandas as pd
import sys
import os
from pathlib import Path
from textwrap import wrap

# Import the bar chart function from our module
from nlesc_ser2026_plots.bar_charts import create_yearly_stacked_bar_chart, create_yearly_multi_bar_chart, create_yearly_stacked_bar_line_chart
from nlesc_ser2026_plots.geo_charts import plot_netherlands_with_institutions
import argparse

def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(description="Generate charts from CSV files in a specified directory.")
    parser.add_argument("input_dir", type=str, help="Path to the directory containing the CSV files.")
    parser.add_argument("--format", type=str, default="png", choices=["html", "png", "svg", "pdf"], help="Output format for the charts.")
    parser.add_argument("--output_dir", type=str, default=".", help="Directory to save the generated charts.")
    return parser.parse_args()

args = parse_arguments()
input_dir = Path(args.input_dir)
if not input_dir.is_dir():
    print(f"Error: The specified input directory '{input_dir}' does not exist or is not a directory.")
    sys.exit(1)
output_dir = Path(args.output_dir)
output_dir.mkdir(parents=True, exist_ok=True)

# Process FTE data
fte_file = input_dir / "example_fte_data.csv"
if os.path.exists(fte_file):
    df_fte = pd.read_csv(fte_file)
    color_variable = 'Activity'
    value_variable = 'Expenditure (FTE)'
    df_long = df_fte.melt(id_vars=['Year'], var_name=color_variable, value_name=value_variable)
    df_long['Activity'] = df_long['Activity'].apply(lambda x: '@'.join(wrap(x, 16)))
    chart = create_yearly_stacked_bar_chart(
        df=df_long,
        y_variable=value_variable,
        color_variable=color_variable,
        title="FTE Allocation by Activity per Year",
        dimensions=[800, 500]
    )
    chart.save(output_dir / f"fte_allocation_chart.{args.format}")


# Make map of spatial collaborations diversity
cities_file = input_dir / "dutch_cities.csv"
if os.path.exists(cities_file):
    cities_df = pd.read_csv(cities_file)
    geo_chart = plot_netherlands_with_institutions(cities_df)
    geo_chart.save(f"netherlands_institutions.{args.format}")

# Make bar charts for funding data
funding_file = input_dir / "example_income_streams.csv"
if os.path.exists(funding_file):
    funding_df = pd.read_csv(funding_file)
    color_variable = 'Income Stream'
    value_variable = 'Income (M€)'
    df_long = funding_df.melt(id_vars=['Year'], var_name=color_variable, value_name=value_variable)
    chart = create_yearly_stacked_bar_chart(
        df=df_long,
        y_variable=value_variable,
        color_variable=color_variable,
        title="Income sources per Year",
        dimensions=[800, 500]
    )
    chart.save(output_dir / f"funding_data_chart.{args.format}")

# Make bar charts for headcount data
headcount_file = input_dir / "example_headcount_data.csv"
if os.path.exists(headcount_file):
    headcount_df = pd.read_csv(headcount_file)
    color_variable = 'Department'
    value_variable = 'Number of Employees'
    df_long = headcount_df.melt(id_vars=['Year'], var_name=color_variable, value_name=value_variable)
    chart = create_yearly_stacked_bar_chart(
        df=df_long,
        y_variable=value_variable,
        color_variable=color_variable,
        title="Number of Employees per Year",
        dimensions=[800, 500]
    )
    chart.save(output_dir / f"headcount_data_chart.{args.format}")


# Make bar-line charts for calls data
calls_file = input_dir / "call_data.csv"
if os.path.exists(calls_file):
    calls_df = pd.read_csv(calls_file)
    value_variable = 'Call budget (MEUR)'
    df_yearly_sums = calls_df.groupby(['Year'], as_index=False).sum()
    # Define constants
    acceptance_rate_variable = 'Acceptance Rate (%)'
    df_yearly_sums[acceptance_rate_variable] = 100 * df_yearly_sums['Acceptances'] / df_yearly_sums['Submissions']
    # Aggregate over 'Year' column and drop the 'Call' column
    calls_df['Call'] = calls_df['Call'].apply(lambda x: 'ASDI/OEC/ETEC' if x in ['ASDI', 'OEC', 'ETEC'] else 'Other')
    df_aggregated = calls_df.groupby(['Year', 'Call'], as_index=False).sum()
    df_aggregated[acceptance_rate_variable] = df_aggregated['Year'].map(df_yearly_sums.set_index('Year')[acceptance_rate_variable])
    bar_line_chart = create_yearly_stacked_bar_line_chart(
        df=df_aggregated,
        title="Submissions and Acceptance Rate Over Years",
        y_variable_left="Submissions",
        y_variable_right=acceptance_rate_variable,
        color_variable="Call",
        dimensions=[800, 500]
    )
    bar_line_chart.save(output_dir / f"calls_bar_line_chart.{args.format}")

    # Add 'Requested budget' and 'Provided budget' columns
    calls_df['Requested'] = (calls_df['In-kind funding per project (kEUR)'] + calls_df['Cash funding per project (kEUR)']) * calls_df['Submissions'] / 1000
    calls_df['Provided'] = (calls_df['In-kind funding per project (kEUR)'] + calls_df['Cash funding per project (kEUR)']) * calls_df['Acceptances'] /1000

    # Aggregate over 'Year' column and drop the 'Call' column
    df_aggregated = calls_df.groupby('Year', as_index=False).sum()
    df_aggregated.set_index('Year', inplace=True)
    df_aggregated = df_aggregated[['Requested', 'Provided']]

    offset_variable = 'Budget'
    df_long = df_aggregated.reset_index().melt(id_vars=['Year'], var_name=offset_variable, value_name=value_variable)
    chart = create_yearly_multi_bar_chart(
        df=df_long,
        title="Requested budget vs approved budget per year",
        y_variable=value_variable,
        offset_variable=offset_variable,
        dimensions=[800, 500]
    )
    chart.save(output_dir / f"calls_multi_bar_chart.{args.format}")

projects_file = input_dir / "project_overview.csv"
if os.path.exists(projects_file):
    ext_proj_df = pd.read_csv(projects_file, index_col=0)
    # Reset index to make year a column if it's currently the index
    if ext_proj_df.index.name is None:
        ext_proj_df.index.name = 'slug'
    
    # Aggregate data by 'call_year' and 'TYPE'
    df_aggregated = ext_proj_df.groupby(['call_year', 'TYPE'], as_index=False)['INCOME'].sum()
    df_aggregated['INCOME'] = df_aggregated['INCOME'] / 1000  # Convert to kEUR

    # Rename columns for clarity
    df_aggregated.rename(columns={'call_year': 'Year', 'TYPE': 'Type', 'INCOME': 'Income (kEUR)'}, inplace=True)

    external_acquisition_chart = create_yearly_stacked_bar_chart(
        df=df_aggregated,
        y_variable="Income (kEUR)",
        color_variable="Type",
        title="External Acquisition per Year",
        dimensions=[800, 500]
    )
    external_acquisition_chart.save(output_dir / f"external_acquisition_per_year.{args.format}")

    journalPapers_file = input_dir / "journalArticles.csv"
    journal_df = pd.DataFrame()
    if os.path.exists(journalPapers_file):
        journal_df = pd.read_csv(journalPapers_file)
        # Filter out records where 'project type' is 'EXTERNAL' and 'author position' is 'none'
        journal_df = journal_df[~((journal_df['project type'] == 'EXTERNAL') & (journal_df['author position'] == 'none'))]
    conferencePapers_file = input_dir / "conferencePapersCurated.csv"
    conference_df = pd.DataFrame()
    if os.path.exists(conferencePapers_file):
        conference_df = pd.read_csv(conferencePapers_file)
        # Filter out records where 'project type' is 'EXTERNAL' and 'author position' is 'none'
        conference_df = conference_df[~((conference_df['project type'] == 'EXTERNAL') & (conference_df['author position'] == 'none'))]
    publications_df = pd.concat([journal_df, conference_df], ignore_index=True)
    # Create new column 'authorship' based on 'author position'
    publications_df['authorship'] = publications_df['author position'].apply(lambda x: 'NLeSC funded' if x == 'none' else 'NLeSC authored')
    # Aggregate data by 'year' and 'authorship'
    df_aggregated = publications_df.groupby(['year', 'authorship'], as_index=False).size()
    print("Publications DataFrame loaded successfully:")
    print(df_aggregated.head())
    df_aggregated.rename(columns={'year': 'Year', 'size': 'Number of Publications'}, inplace=True)
    publications_chart = create_yearly_stacked_bar_chart(
        df=df_aggregated,
        y_variable="Number of Publications",
        color_variable="authorship",
        title="Peer-reviewed publications per year",
        dimensions=[800, 500]
    )
    publications_chart.save(output_dir / f"publications_per_year.{args.format}")
    



