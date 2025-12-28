#!/usr/bin/env python3
"""Example script demonstrating how to create a stacked bar chart from CSV data.

This script shows how to:
1. Read FTE data from a CSV file
2. Process the data for visualization
3. Create a stacked bar chart using the create_stacked_bar_chart function
4. Display and optionally save the chart

Usage:
    python example_usage.py [csv_file_path]

If no csv_file_path is provided, it will use the default example_fte_data.csv
"""

import pandas as pd
import sys
import os
from pathlib import Path

# Import the bar chart function from our module
from nlesc_ser2026_plots.bar_charts import create_stacked_bar_chart


def main():
    """Main function to demonstrate chart creation from CSV data."""
    # Determine CSV file path
    if len(sys.argv) > 1:
        csv_file = sys.argv[1]
    else:
        # Use the example CSV file in the project root
        project_root = Path(__file__).parent
        csv_file = project_root / "example_fte_data.csv"
    
    # Check if file exists
    if not os.path.exists(csv_file):
        print(f"Error: CSV file '{csv_file}' not found!")
        print("Please provide a valid CSV file path or ensure example_fte_data.csv exists.")
        sys.exit(1)
    
    print(f"Reading data from: {csv_file}")
    
    try:
        # Read the CSV file
        # Assume the first column contains years and subsequent columns are activities
        df = pd.read_csv(csv_file, index_col=0)
        
        print(f"Data loaded successfully!")
        print(f"Shape: {df.shape}")
        print(f"Years: {df.index.tolist()}")
        print(f"Activities: {df.columns.tolist()}")
        print("\\nFirst few rows:")
        print(df.head())
        
        # Create the stacked bar chart
        print("\\nCreating stacked bar chart...")
        chart = create_stacked_bar_chart(
            df=df,
            title="FTE Allocation by Activity per Year",
            width=800,
            height=500
        )
        
        print("Chart created successfully!")
        
        # Display the chart
        print("Displaying chart...")
        chart.show()
        
        # Optionally save the chart
        save_choice = input("\\nWould you like to save the chart as HTML? (y/n): ").lower().strip()
        if save_choice in ['y', 'yes']:
            output_file = input("Enter output filename (default: fte_chart.html): ").strip()
            if not output_file:
                output_file = "fte_chart.html"
            
            if not output_file.endswith('.html'):
                output_file += '.html'
            
            chart.save(output_file)
            print(f"Chart saved as '{output_file}'")
        
        print("\\nExample completed successfully!")
        
    except FileNotFoundError:
        print(f"Error: Could not find file '{csv_file}'")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: The CSV file '{csv_file}' is empty")
        sys.exit(1)
    except Exception as e:
        print(f"Error processing the data: {str(e)}")
        sys.exit(1)


def create_sample_data():
    """Create a sample CSV file with FTE data for demonstration."""
    sample_data = {
        'Research Projects': [2.1, 2.5, 3.0, 2.8, 3.2],
        'Trainings': [0.8, 1.0, 1.2, 1.5, 1.3],
        'Community Building': [0.3, 0.5, 0.8, 0.7, 0.9],
        'Administration': [0.4, 0.5, 0.6, 0.7, 0.8],
        'Consultancy': [0.2, 0.3, 0.4, 0.5, 0.6]
    }
    
    years = list(range(2020, 2025))
    df = pd.DataFrame(sample_data, index=years)
    df.index.name = 'Year'
    
    output_file = "sample_fte_data.csv"
    df.to_csv(output_file)
    print(f"Sample data created and saved as '{output_file}'")
    return output_file


if __name__ == "__main__":
    # Check if user wants to create sample data
    if len(sys.argv) > 1 and sys.argv[1] == "--create-sample":
        create_sample_data()
    else:
        main()