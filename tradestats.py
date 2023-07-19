import sys
import os
import pandas as pd
from datetime import datetime

def analyze_trades(file_name):
    # Load a few rows to get the column names
    df_sample = pd.read_csv(file_name, nrows=5)
    column_names = df_sample.columns.tolist()

    # Exclude the "Deploy" column
    usecols = column_names[1:]

    # Load the CSV file into a DataFrame, ignoring the "Deploy" column
    df = pd.read_csv(file_name, usecols=usecols)

    #print(os.listdir(os.getcwd()))
    # Load the CSV file into a DataFrame
    df = pd.read_csv(file_name)

    # Convert Time column to datetime
    df['Time'] = pd.to_datetime(df['Time'])

    # Sort dataframe by Time
    df = df.sort_values(by='Time')

    # Identify the start of each cycle (buy trades) and the end of each cycle (sell trades)
    start_of_cycles = df[df['Quantity'] > 0].index
    end_of_cycles = df[df['Quantity'] < 0].index

    # Ensure that each start has a corresponding end
    if len(start_of_cycles) > len(end_of_cycles):
        start_of_cycles = start_of_cycles[:len(end_of_cycles)]
    elif len(start_of_cycles) < len(end_of_cycles):
        end_of_cycles = end_of_cycles[:len(start_of_cycles)]

    # Create paired indices for start and end of cycles
    paired_indices = list(zip(start_of_cycles, end_of_cycles))

    # Calculate profit for each trade cycle
    profits_per_cycle = [df.loc[end, 'Price'] * abs(df.loc[end, 'Quantity']) - df.loc[start, 'Price'] * df.loc[start, 'Quantity'] for start, end in paired_indices]
    total_profit = sum(profits_per_cycle)

    # Calculate average days for a trade cycle (buy-sell)
    trade_cycle_durations = [(df.loc[end, 'Time'] - df.loc[start, 'Time']).total_seconds() / 86400 for start, end in paired_indices]  # convert seconds to days
    avg_days_trade_cycle = sum(trade_cycle_durations) / len(trade_cycle_durations)

    # Calculate average days between trade cycles (sell-buy)
    between_cycle_durations = [(df.loc[start, 'Time'] - df.loc[end, 'Time']).total_seconds() / 86400 for start, end in zip(start_of_cycles[1:], end_of_cycles[:-1])]  # convert seconds to days
    avg_days_between_cycles = sum(between_cycle_durations) / len(between_cycle_durations)

    # Convert durations to hours for a more precise measure
    avg_hours_trade_cycle = avg_days_trade_cycle * 24
    avg_hours_between_cycles = avg_days_between_cycles * 24

    # Calculate the total time frame for all trades
    total_time_frame = (df['Time'].max() - df['Time'].min()).total_seconds() / 3600  # convert seconds to hours

    # Calculate the date range for all trades
    start_date = df['Time'].min()
    end_date = df['Time'].max()

    return total_profit, avg_hours_trade_cycle, avg_hours_between_cycles, total_time_frame, start_date, end_date

print(analyze_trades("/content/drive/MyDrive/data/colab/live_trades_1688566344_1689268879_L-84c5ddfca0a8fdbea2aef37f5ea62fc0.csv.gsheet"))
