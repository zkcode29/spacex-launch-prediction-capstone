import pandas as pd
import os

def scrape_launch_data(wiki_url="https://en.wikipedia.org/wiki/List_of_Falcon_9_and_Falcon_Heavy_launches"):
    """
    Scrapes Falcon 9 launch data from a Wikipedia page using pandas.

    Args:
        wiki_url (str): The URL of the Wikipedia page to scrape.

    Returns:
        pd.DataFrame: A DataFrame containing the launch data, or None if scraping fails.
    """
    print(f"Scraping data from {wiki_url}...")
    try:
        # pandas.read_html is a powerful tool for scraping tables from web pages
        tables = pd.read_html(wiki_url)
        
        # I need to find the correct tables that contain the launch records.
        # I will combine all tables that have a "Flight No." column.
        launch_df = pd.concat(
            [table for table in tables if "Flight No." in table.columns or "Flight\nNo." in table.columns],
            ignore_index=True
        )
        print("Scraping successful.")
        return launch_df
    except Exception as e:
        print(f"Error scraping data: {e}")
        return None

def save_data_as_csv(dataframe, path, filename):
    """
    Saves a pandas DataFrame to a specified path as a CSV file.

    Args:
        dataframe (pd.DataFrame): The DataFrame to save.
        path (str): The directory path to save the file in.
        filename (str): The name of the file.
    """
    if dataframe is not None:
        if not os.path.exists(path):
            os.makedirs(path)
        filepath = os.path.join(path, filename)
        dataframe.to_csv(filepath, index=False)
        print(f"Data saved to {filepath}")
    else:
        print("No data to save.")

if __name__ == '__main__':
    DATA_PATH = 'data/raw'
    FILENAME = 'wiki_falcon9_table.csv'
    
    scraped_data = scrape_launch_data()
    save_data_as_csv(scraped_data, DATA_PATH, FILENAME)