  
import tkinter as tk
from tkinter import ttk
  
import tkinter as tk
from tkinter import ttk

def create_search_dialog(master):
    # Create a new top-level window for the search dialog
    search_window = tk.Toplevel(master)
    search_window.title('Amplifier Search')
    search_window.geometry('500x200')
    ttk.Label(search_window, text="The search option:", font=("Times New Roman", 10)).grid(column=0, row=5, padx=10, pady=25)

    # Combobox creation
    n = tk.StringVar()
    search_opt = ttk.Combobox(search_window, width=27, textvariable=n)

    # Adding combobox drop-down list
    search_opt['values'] = ('Serial number', 'Model string', 'Manufacturer')
    search_opt.grid(column=1, row=5)

    # Label for input field
    ttk.Label(search_window, text="Enter search string:", font=("Times New Roman", 10)).grid(column=0, row=2, padx=10, pady=10)

    # Entry field for inputting the search string
    entry = ttk.Entry(search_window, width=30)
    entry.grid(column=1, row=2, padx=10, pady=10)

    result = {"option": None, "string": None}
    def on_search():
        result["option"] = search_opt.get()
        result["string"] = entry.get()
        search_window.destroy()

    search_button = ttk.Button(search_window, text="Search", command=on_search)
    search_button.grid(column=1, row=10, pady=20)

    return result # Return the ComboBox and Entry for use in the main application
