import os
import datetime
from google.cloud import bigquery
import pandas as pd

# Function to get the maximum date from the existing CSV file
def get_max_date_from_csv(csv_file_path):
    if os.path.isfile(csv_file_path):
        df = pd.read_csv(csv_file_path)
        if not df.empty:
            return pd.to_datetime(df['Day']).max()
    return None


client = bigquery.Client()

project_id = 'bigquery-turkey-search'

csv_file_path = "archive.csv"

max_date_in_csv = get_max_date_from_csv(csv_file_path)

if max_date_in_csv:
    start_date = max_date_in_csv.strftime('%Y-%m-%d')
else:
    start_date = '2024-01-01'

query = f"""
    SELECT
        refresh_date AS Day,
        term AS Top_Term,
        rank
    FROM `bigquery-public-data.google_trends.international_top_terms`
    WHERE
        country_name = "Turkey"
        AND rank <= 3
        AND refresh_date >= "{start_date}"
    GROUP BY Day, Top_Term, rank
    ORDER BY Day DESC, rank ASC;
"""

query_job = client.query(query)

df = query_job.to_dataframe()

existing_df = pd.read_csv(csv_file_path) if os.path.isfile(csv_file_path) else pd.DataFrame()
updated_df = pd.concat([existing_df, df], ignore_index=True)

updated_df.to_csv(csv_file_path, index=False)




