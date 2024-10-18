import pandas as pd
import re

def load_data(filepath):
    """
    Loads data from a CSV file into a DataFrame.

    Args:
    filepath (str): The path to the CSV file to be loaded.

    Returns:
    DataFrame: The loaded data.
    """
    try:
        data = pd.read_csv(filepath)
        print(f"Data successfully loaded from {filepath}")
        return data
    except FileNotFoundError:
        print(f"Error: The file {filepath} does not exist.")
    except Exception as e:
        print(f"An error occurred while loading the data: {e}")
    print("load_data done")

def merge_data(actual_data, extracted_data, key='Invoice Number'):
    """
    Merges two datasets on a specified key.

    Args:
    actual_data (DataFrame): The DataFrame containing the ground truth data.
    extracted_data (DataFrame): The DataFrame containing the data extracted from invoices.
    key (str): The column to merge the data on.

    Returns:
    DataFrame: The merged DataFrame.
    """
    # Ensure 'Invoice Number' is of type string
    actual_data['Invoice Number'] = actual_data['Invoice Number'].astype(str)
    extracted_data['Invoice Number'] = extracted_data['Invoice Number'].astype(str)

    try:
        # Merge for accuracy comparison based on Invoice Number
        merged = pd.merge(actual_data, extracted_data, on='Invoice Number', suffixes=('_true', '_pred'))
        print(f"Data successfully merged on {key}")
        return merged
    except Exception as e:
        print(f"An error occurred during data merging: {e}")








