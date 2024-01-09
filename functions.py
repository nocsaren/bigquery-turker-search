import os
import pandas as pd
import tkinter as tk
from datetime import datetime
from google.cloud import bigquery
from tkcalendar import DateEntry
import pyperclip
import locale

def set_locale():
    locale.setlocale(locale.LC_TIME, "tr_TR")

def generate_post(date, csv_file_path="archive.csv"):
    formatted_date = datetime.strptime(date, "%Y-%m-%d").strftime("%#d %B %Y")

    if not os.path.isfile(csv_file_path):
        return f"The file {csv_file_path} not found."

    df = pd.read_csv(csv_file_path)
    filtered_df = df[df["Day"] == date]

    if not filtered_df.empty:
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
        result_string = f"No data for {formatted_date}."

    return result_string

def copy_to_clipboard(result_text):
    text_to_copy = result_text.get("1.0", "end-1c") 
    pyperclip.copy(text_to_copy)

def update_post(date_entry, result_text):
    new_date = date_entry.get_date().strftime("%Y-%m-%d")
    new_text = generate_post(new_date)
    result_text.config(state=tk.NORMAL)
    result_text.delete("1.0", tk.END)
    result_text.insert(tk.END, new_text)
    result_text.config(state=tk.DISABLED)

def create_gui(root, initial_date):
    set_locale()

    # Calendar widget for user to select the date
    date_label = tk.Label(root, text="Select Date:")
    date_label.pack()

    date_entry = DateEntry(root, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd')
    date_entry.set_date(initial_date)  # Set initial date
    date_entry.pack(pady=5)

    # Bind the <FocusOut> event to update the post dynamically ***GLITCHY***
    date_entry.bind("<FocusOut>", lambda event: update_post(date_entry, result_text))

    # Generate the initial post
    text = generate_post(initial_date)

    # Create and pack a Text widget to display the text
    result_text = tk.Text(root, wrap=tk.WORD, height=10, width=50)
    result_text.insert(tk.END, text)
    result_text.pack(padx=10, pady=10)

    # Button to copy the text to clipboard
    copy_button = tk.Button(root, text="Copy to Clipboard", command=lambda: copy_to_clipboard(result_text))
    copy_button.pack(pady=10)

    # Allow text to be selectable and copyable
    result_text.config(state=tk.NORMAL)
    result_text.tag_configure("center", justify="center")
    result_text.tag_add("center", "1.0", "end")
    result_text.config(state=tk.DISABLED)

    return date_entry, result_text

def fetch_and_update_archive(csv_file_path):
    client = bigquery.Client()
    project_id = 'bigquery-turkey-search'

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

def get_max_date_from_csv(csv_file_path):
    if os.path.isfile(csv_file_path):
        df = pd.read_csv(csv_file_path)
        if not df.empty:
            return pd.to_datetime(df['Day']).max()
    return None
