from datetime import datetime
import tkinter as tk
from functions import create_gui, fetch_and_update_archive, update_post

def fetch_button_callback():
    fetch_and_update_archive("archive.csv")
    update_post(date_entry, result_text)

if __name__ == "__main__":
    initial_date = datetime.now().strftime("%Y-%m-%d")

    root = tk.Tk()
    root.title("Generated Post")

    date_entry, result_text = create_gui(root, initial_date)

    fetch_button = tk.Button(root, text="Fetch", command=fetch_button_callback) #   ***NOT THROUGHLY TESTED***
    fetch_button.pack(pady=10)

    root.mainloop()
