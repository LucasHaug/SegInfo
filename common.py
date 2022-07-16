import os

import tkinter as tk
from tkinter import messagebox


PUBLIC_KEY_FILE_NAME = "public_key.pem"
PRIVATE_KEY_FILE_NAME = "private_key.pem"


def list_files(base_dir):
    all_files = []

    for path, _, files in os.walk(base_dir):
        for name in files:
            # TODO: Fix to work with all file types
            if name.endswith(".txt"):
                all_files.append(os.path.join(path, name))

    return all_files


def show_pop_up(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()