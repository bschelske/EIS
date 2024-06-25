import pandas as pd
import os
import matplotlib.pyplot as plt
from typing import Union, Any


def get_file_paths(parent_dir: str) -> list[str]:
    """Get .txt files from a directory"""
    file_list = [parent_dir + f for f in os.listdir(parent_dir) if f.endswith('.txt')]
    return file_list


def open_file_as_df(file_path: str) -> tuple[Any, str]:
    """Open EIS txt file generated from CH Instrument, make into a pandas dataframe."""

    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Separate the header and the data
    header_lines = []
    data_lines = []
    data_start = False
    for line in lines:
        if line.strip() == 'Freq/Hz, Z\'/ohm, Z"/ohm, Z/ohm, Phase/deg':
            data_start = True
            header_lines.append(line.strip())
        elif data_start:
            data_lines.append(line.strip())
        else:
            header_lines.append(line.strip())

    # Display the header information
    header_info = "\n".join(header_lines[:11])

    # Create a DataFrame from the data
    data = [line.split(', ') for line in data_lines]
    df = pd.DataFrame(data, columns=['Freq/Hz', 'Z\'/ohm', 'Z"/ohm', 'Z/ohm', 'Phase/deg'])

    # Convert columns to appropriate data types
    df = df.apply(pd.to_numeric)
    df = df.drop(index=0).reset_index(drop=True)
    return df, header_info


def min_x_max_y(tuple1, tuple2):
    x1, y1 = tuple1
    x2, y2 = tuple2

    min_x = min(x1, x2)
    max_y = max(y1, y2)

    return min_x, max_y

def nyquist_plot(df: pd.DataFrame) -> Union[Any, Any]:
    """Create nyquist plot from a pandas dataframe"""
    fig, ax = plt.subplots()
    ax.plot(df["Z'/ohm"], df['Z"/ohm']*-1)

    # Each axis range should be equal
    new_limit = min_x_max_y(ax.get_xlim(), ax.get_ylim())
    print(ax.get_xlim())
    print(ax.get_ylim())
    print(new_limit)
    ax.set_xlim(new_limit)
    ax.set_ylim(new_limit)

    ax.set_xlabel("Z'/ohm")
    ax.set_ylabel('-Z"/ohm')
    ax.spines[['right', 'top']].set_visible(False)
    ax.set_title('file')
    return fig, ax


def compare_nyquist(df_list: list[pd.DataFrame]) -> Union[Any, Any]:
    """Makes single nyquist plot from list of pandas dataframes"""

    fig, ax = plt.subplots()
    for df in df_list:
        ax.plot(df["Z'/ohm"], df['Z"/ohm']*-1)

    ax.set_xlabel("Z'/ohm")
    ax.set_ylabel('-Z"/ohm')
    ax.spines[['right', 'top']].set_visible(False)
    return fig, ax


def bode_plot(df: pd.DataFrame) -> Union[Any, Any]:
    """Makes single nyquist plot from list of pandas dataframes"""

    fig, axes = plt.subplots(2,1)
    axes[0].plot(df["Z'/ohm"], df['Z"/ohm']*-1)
    axes[0].set_xlabel("Z'/ohm")
    axes[0].set_ylabel('-Z"/ohm')
    axes[0].spines[['right', 'top']].set_visible(False)

    axes[1].plot(df["Z'/ohm"], df['Z"/ohm'] * -1)
    axes[1].set_xlabel("Z'/ohm")
    axes[1].set_ylabel('-Z"/ohm')
    axes[1].spines[['right', 'top']].set_visible(False)
    return fig, axes


def main():
    path = "data/11/"
    files = get_file_paths(path)
    file = files[0]
    df, file_information = open_file_as_df(file)

    # Create a nyquist plot
    nyquist_fig, nyquist_ax = nyquist_plot(df)
    nyquist_ax.set_title(file)
    plt.show()

    """
    # Process many files
    dataframes = []
    for file in files:
        df, info = open_file_as_df(file)
        dataframes.append(df)
    
    # print(df)
    fig, ax = compare_nyquist(dataframes)
    ax.set_title(files)
    plt.show()
    #
    # bode_plot(df)
    # plt.show()
    # # If you want to save the DataFrame to a CSV file
    # df.to_csv('trial_1.csv', index=False)
    """

if __name__ == "__main__":
    main()