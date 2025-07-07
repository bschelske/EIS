import pandas as pd
import os
from main import get_file_paths, open_file_as_df


def get_folders(parent_dir: str) -> list[str]:
    """Get folders from a directory"""
    folder_list = [f.path + '\\' for f in os.scandir(parent_dir) if f.is_dir()]
    return folder_list


def transform_df(df):
    df_melted = df.melt(id_vars='Freq/Hz', var_name='variable')
    # Create a label column
    df_melted["Label"] = df_melted["variable"] +'_'+ df_melted["Freq/Hz"].astype(str)
    # Transpose
    df_melted = df_melted.T

    # Extract Information
    headers = df_melted.loc['Label']
    values = df_melted.loc['value'].values
    transformed_df = pd.DataFrame([values], columns=headers)
    return transformed_df


def main():
    path = 'path'
    folders = get_folders(path)
    all_files = pd.DataFrame()
    for folder in folders:
        files = get_file_paths(folder)
        for file in files:
            df, header_info = open_file_as_df(file)
            print(df.columns)
            temp_df = transform_df(df)
            print(file)
            temp_df['file'] = file
            all_files = pd.concat([all_files, temp_df]).dropna(axis='columns')
    # print(all_files.dropna(axis='columns'))

    all_files.to_csv("results/EIS.csv")


if __name__ == '__main__':
    main()