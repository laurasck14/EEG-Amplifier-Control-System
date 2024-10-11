  
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Frame, Label, Entry, Button
from Amplifier import EEGAmplifierControlSystem

  
# Creating tkinter window
window = tk.Tk()
window.title('Amplifier search')
window.geometry('500x200')
  
# label text for title
ttk.Label(window,
          font = ("Times New Roman", 15)).grid(row = 0, column = 1)
  
# label
ttk.Label(window, text = "The search option :",
          font = ("Times New Roman", 10)).grid(column = 0,
          row = 5, padx = 10, pady = 25)
  
# Combobox creation
n = tk.StringVar()
search_opt = ttk.Combobox(window, width = 27, textvariable = n)
  
# Label for input field
ttk.Label(window, text="Enter search string:", font=("Times New Roman", 10)).grid(column=0, row=2, padx=10, pady=10)

# Entry field for inputting the search string
entry = ttk.Entry(window, width=30)
entry.grid(column=1, row=2, padx=10, pady=10)

# Adding combobox drop down list
search_opt['values'] = ('Serial number', 'Model string', 'Manufacturer')
search_opt.grid(column = 1, row = 5)
search_opt.current()



# Search button to trigger the search function
#search_button = ttk.Button(window, text="Search", command=search_amplifier)
#search_button.grid(column=1, row=3, pady=20)
window.mainloop()