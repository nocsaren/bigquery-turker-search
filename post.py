import os
import pandas as pd
from datetime import datetime
import locale
Date = "2024-01-05"
csv_file_path = "archive.csv"
locale.setlocale(locale.LC_TIME, "tr_TR")

def generate_post(Date):
    if not os.path.isfile(csv_file_path):
        return f"The file {csv_file_path} not found."
    
    df = pd.read_csv(csv_file_path)
    filtered_df = df[df["Day"] == Date]
    
    if not filtered_df.empty:
        formatted_date = datetime.strptime(Date, "%Y-%m-%d").strftime("%#d %B %Y")

        top_term_1 = filtered_df["Top_Term"][filtered_df["rank"]==1].values[0]
        top_term_2 = filtered_df["Top_Term"][filtered_df["rank"]==2].values[0]
        top_term_3 = filtered_df["Top_Term"][filtered_df["rank"]==3].values[0]

        result_string = (
            f"{formatted_date} tarihinde Türkiye'den en çok yapılan 3 Google araması:\n"
            f"1- {top_term_1}\n"
            f"2- {top_term_2}\n"
            f"3- {top_term_3}\n"
            f"#BigQuery"
        )
    else:
        result_string = f"No data for {Date}."

    return result_string

text = generate_post(Date)
print(text)