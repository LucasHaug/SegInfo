import os

import tkinter as tk
from tkinter import messagebox

PUBLIC_ASYM_KEY_FILE_NAME = "public_asym_key.pem"
PRIVATE_ASYM_KEY_FILE_NAME = "private_asym_key.pem"

SYM_KEY_FILE_NAME = "sym_key.key"

def list_files(base_dir):
    all_files = []

    for path, _, files in os.walk(base_dir):
        for name in files:
            all_files.append(os.path.join(path, name))

    return all_files


def show_pop_up(title, message):
    root = tk.Tk()
    root.withdraw()
    messagebox.showerror(title, message)
    root.destroy()