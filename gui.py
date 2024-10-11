#!/usr/bin/env python3
''' Laura Santa Cruz Kaster
usage: python3 gui.py
'''
import sys, os, re
import tkinter as tk
import tkinter.ttk as ttk
from GuiBaseClass import GuiBaseClass
import tkinter.filedialog as filedialog
from tkinter import simpledialog, messagebox
from Amplifier import EEGAmplifierControlSystem, Amplifier, Sensor
from datetime import datetime


class EEGAmplifier(GuiBaseClass):
    def __init__(self, root, args):
        super().__init__(root)

        self.control_system = EEGAmplifierControlSystem()

        mnu=self.getMenu('Amplifier')
        mnu.add_command(label='Add new amplifier', command=self.add_new_amplifier)

        mf = self.getFrame()
        self.pw = ttk.PanedWindow(mf, orient='horizontal')

        self.lb_files = tk.Listbox(self.pw,exportselection=True)
        self.lb_opt = tk.Listbox(self.pw,exportselection=False)
        self.pw.add(self.lb_files)
        self.lb_opt.insert(1,'Remove')
        self.lb_opt.insert(2,'Information')
        self.pw.add(self.lb_opt)

        self.text = tk.Text(self.pw, wrap='word',undo=True)
        self.pw.add(self.text)
        self.pw.pack(side='top', fill='both', expand=True)

    def add_new_amplifier(self):
        """Prompt user for amplifier details and add it to the control system."""
        try:
            serial_number = simpledialog.askstring("Input", "Enter Serial Number:")
            model = simpledialog.askstring("Input", "Enter Model:")
            manufacturer = simpledialog.askstring("Input", "Enter Manufacturer:")
            next_maintenance = simpledialog.askstring("Input", "Enter Next Maintenance Date (YYYY-MM-DD):")
            sampling_rate = simpledialog.askinteger("Input", "Enter Sampling Rate (256, 512, 1024):")
            gain = simpledialog.askinteger("Input", "Enter Gain (1-100):")

            # Validate date input
            try:
                next_maintenance_date = datetime.strptime(next_maintenance, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Invalid Date", "Date format should be YYYY-MM-DD")
                return

            # Create amplifier
            amplifier = Amplifier(serial_number=serial_number, model=model, manufacturer=manufacturer,
                                next_maintenance=next_maintenance_date, sampling_rate=sampling_rate, gain=gain)
            
            # Add amplifier to the control system
            self.control_system.register_amplifier(amplifier)
            
            # Update the amplifier list in the GUI
            self.lb_files.insert(tk.END, serial_number)

        except Exception as e:
            messagebox.showerror("Error", str(e))

        def selection(event):
            if not self.lb_files.curselection():
                self.message("Please select an amplifier")

            elif self.lb_files.curselection():
                amplifier = self.lb_files.get(self.lb_files.curselection())
                opt = self.lb_opt.get(self.lb_opt.curselection())

                # if 'GO' in opt:
                #     sol = amplifier.get_go_ids(amplifier)
                #     self.text.insert('1.0',sol)
                    
        self.lb_opt.bind('<Double-1>', selection)


def main (args):
    root=tk.Tk()
    root.geometry("800x600")
    root.title("EEG Amplifier Control System")
    bapp = EEGAmplifier(root, args) 
    bapp.mainLoop()

if __name__ == "__main__":
   main(sys.argv)