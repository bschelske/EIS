import pandas as pd
import os
import numpy as np
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
    ax.plot(df["Z'/ohm"], df['Z"/ohm'] * -1)

    # Each axis range should be equal
    new_limit = min_x_max_y(ax.get_xlim(), ax.get_ylim())
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
        ax.plot(df["Z'/ohm"], df['Z"/ohm'] * -1)

    ax.set_xlabel("Z'/ohm")
    ax.set_ylabel('-Z"/ohm')
    ax.spines[['right', 'top']].set_visible(False)
    return fig, ax


def bode_plot(df: pd.DataFrame) -> Union[Any, Any]:
    """Makes single bode plot from pandas dataframe"""

    fig, axes = plt.subplots(2, 1, figsize=(7, 6.66))
    x = np.log10(df['Freq/Hz'])

    # Log(|Z|) vs Log(Frequency)
    axes[0].plot(x, np.log10(df["Z/ohm"].abs()))
    axes[0].set_ylim(0, 7)
    axes[0].set_xlabel("log(Freq/Hz)")
    axes[0].set_ylabel("log(Z/ohm)")
    axes[0].spines[['right', 'top']].set_visible(False)

    # -Phase vs Log(Frequency)
    axes[1].plot(x, df['Phase/deg'] * -1)
    axes[1].set_xlabel("log(Freq/Hz)")
    axes[1].set_ylabel('-Phase/deg')
    axes[1].spines[['right', 'top']].set_visible(False)
    return fig, axes


def bode_plot_overlay(df: pd.DataFrame) -> Union[Any, Any]:
    """Makes bode plot with overlay from pandas dataframe"""

    fig, ax1 = plt.subplots(figsize=(3.33, 3.33))
    ax2 = ax1.twinx()
    x = np.log10(df['Freq/Hz'])

    # Log(|Z|) vs Log(Frequency)
    ax1.plot(x, np.log10(df["Z/ohm"].abs()), color='black', label='|Z|')
    # ax1.set_ylim(0, 7)
    ax1.set_xlabel("log(Freq/Hz)")
    ax1.set_ylabel("log(Z/ohm)")

    # -Phase vs Log(Frequency)
    ax2.plot(x, df['Phase/deg'] * -1, color='red', label='phase')
    # ax2.set_ylim(ax2.get_ylim()[0] - 40, ax2.get_ylim()[1] + 40)
    ax2.set_xlabel("log(Freq/Hz)")
    ax2.set_ylabel('-Phase/deg')
    fig.legend(loc="upper right", bbox_to_anchor=(1,1), bbox_transform=ax1.transAxes)

    return fig, ax1


def nyquist_and_bode(df: pd.DataFrame) -> Union[Any, Any]:
    """Makes nyquist and bode plot from pandas dataframe"""

    fig, ax1 = plt.subplots(1,2, figsize=(7, 3.5))
    plt.gcf().subplots_adjust(bottom=0.15)

    ax1[0].plot(df["Z'/ohm"], df['Z"/ohm'] * -1)

    # Each axis range should be equal
    new_limit = min_x_max_y(ax1[0].get_xlim(), ax1[0].get_ylim())
    ax1[0].set_xlim(new_limit)
    ax1[0].set_ylim(new_limit)

    ax1[0].set_xlabel("Z'/ohm")
    ax1[0].set_ylabel('-Z"/ohm')
    ax1[0].spines[['right', 'top']].set_visible(False)

    ax2 = ax1[1].twinx()
    x = np.log10(df['Freq/Hz'])

    # Log(|Z|) vs Log(Frequency)
    ax1[1].plot(x, np.log10(df["Z/ohm"].abs()), color='black', label='|Z|')
    # ax1.set_ylim(0, 7)
    ax1[1].set_xlabel("log(Freq/Hz)")
    ax1[1].set_ylabel("log(Z/ohm)")

    # -Phase vs Log(Frequency)
    ax2.plot(x, df['Phase/deg'] * -1, color='red', label='phase')
    # ax2.set_ylim(ax2.get_ylim()[0] - 40, ax2.get_ylim()[1] + 40)
    ax2.set_xlabel("log(Freq/Hz)")
    ax2.set_ylabel('-Phase/deg')
    fig.legend(loc="lower left", bbox_to_anchor=(0, 0), bbox_transform=ax1[1].transAxes, frameon=False)

    return fig, ax1


def compare_both(df_list: list[pd.DataFrame]) -> Union[Any, Any]:
    """Makes nyquist and bode plot from pandas dataframe"""

    fig, ax1 = plt.subplots(1,2, figsize=(7, 3.5))
    plt.gcf().subplots_adjust(bottom=0.15)
    ax2 = ax1[1].twinx()
    for df in df_list:
        ax1[0].plot(df["Z'/ohm"], df['Z"/ohm'] * -1)
        x = np.log10(df['Freq/Hz'])

        # Log(|Z|) vs Log(Frequency)
        ax1[1].plot(x, np.log10(df["Z/ohm"].abs()), color='black', label='|Z|')

        # -Phase vs Log(Frequency)
        ax2.plot(x, df['Phase/deg'] * -1, color='red', label='phase')

    # Each axis range should be equal
    new_limit = min_x_max_y(ax1[0].get_xlim(), ax1[0].get_ylim())
    ax1[0].set_xlim(new_limit)
    ax1[0].set_ylim(new_limit)
    # ax1[1].set_ylim(0, 7)

    ax1[0].set_xlabel("Z'/ohm")
    ax1[0].set_ylabel('-Z"/ohm')
    ax1[0].spines[['right', 'top']].set_visible(False)

    ax1[1].set_xlabel("log(Freq/Hz)")
    ax1[1].set_ylabel("log(Z/ohm)")
    # ax2.set_ylim(ax2.get_ylim()[0] - 40, ax2.get_ylim()[1] + 40)
    ax2.set_xlabel("log(Freq/Hz)")
    ax2.set_ylabel('-Phase/deg')

    # fig.legend(loc="lower left", bbox_to_anchor=(0, 0), bbox_transform=ax1[1].transAxes, frameon=False)

    return fig, ax1


def main():
    path = "data/7/"
    files = get_file_paths(path)
    file = files[0]
    df, file_information = open_file_as_df(file)
    df.to_csv("7.csv")


    # Create a nyquist plot
    nyquist = False
    if nyquist:
        nyquist_fig, nyquist_ax = nyquist_plot(df)
        nyquist_ax.set_title(file)
        plt.show()

    # Create a Bode plot
    bode = False
    if bode:
        # bode_fig, bode_ax = bode_plot(df)
        # bode_ax[0].set_title(file)

        bode_fig, bode_ax = bode_plot_overlay(df)
        bode_ax.set_title(file)
        plt.show()

    # Create Nyquist and Bode
    both = False
    if both:
        both_fig, both_ax = nyquist_and_bode(df)
        plt.show()

    both_comparison = False
    if both_comparison:
        device = "resistor"
        path = f"data/{device}/"
        files = get_file_paths(path)
        df_list = []
        print(files)

        for file in files:
            df, _ = open_file_as_df(file)
            df_list.append(df)

        fig, ax = compare_both(df_list)
        plt.show()
        fig.savefig(f"C:/Users/bensc/Desktop/Local Research/EIS/plots/{device}_bn.png")


if __name__ == "__main__":
    main()
