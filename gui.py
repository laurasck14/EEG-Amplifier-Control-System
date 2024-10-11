#!/usr/bin/env python3
''' Laura Santa Cruz Kaster
usage: python3 gui.py
'''
import sys, os, re
import tkinter as tk
import tkinter.ttk as ttk
from GuiBaseClass import GuiBaseClass
from tkinter import simpledialog, messagebox
from Amplifier import EEGAmplifierControlSystem, Amplifier, Sensor
from datetime import datetime
from two_input import create_search_dialog


class EEGAmplifier(GuiBaseClass):
    def __init__(self, root, args):
        super().__init__(root)

        self.control_system = EEGAmplifierControlSystem()

        mnu=self.getMenu('Amplifier')
        mnu.add_command(label='List all', command=self.list_all)
        mnu.add_command(label='Add new amplifier', command=self.add_new_amplifier)
        mnu.add_command(label='Search amplifier', command=self.search_for_amplifier)

        mf = self.getFrame()
        self.pw = ttk.PanedWindow(mf, orient='horizontal')

        self.lb_files = tk.Listbox(self.pw, exportselection=True)
        self.lb_opt = tk.Listbox(self.pw, exportselection=False)
        self.pw.add(self.lb_files)
        self.lb_opt.insert(1,'Information')
        self.lb_opt.insert(2,'Remove')
        self.pw.add(self.lb_opt)

        self.text = tk.Text(self.pw, wrap='word',undo=True)
        self.pw.add(self.text)
        self.pw.pack(side='top', fill='both', expand=True)

        # MESSAGES!!!!
        def selection(event):
            if not self.lb_files.curselection():
                self.message("Please select an amplifier")
                return
            
            serial_number = self.lb_files.get(self.lb_files.curselection())
            amplifier = self.control_system.search_amplifier(serial_number=serial_number)[0]
            opt = self.lb_opt.get(self.lb_opt.curselection())

            if 'Information' in opt:
                details = f"Serial Number: {amplifier.serial_number}\n" \
                            f"Model: {amplifier.model}\n" \
                            f"Manufacturer: {amplifier.manufacturer}\n" \
                            f"Next Maintenance: {amplifier.next_maintenance.strftime('%Y-%m-%d')}\n" \
                            f"Sampling Rate: {amplifier.sampling_rate} Hz\n" \
                            f"Gain: {amplifier.gain}\n" \
                            f"Power Status: {'On' if amplifier.is_on else 'Off'}\n" \
                            f"Sensors: {', '.join([sensor.tag for sensor in amplifier.sensors])}"
                self.text.delete('1.0', tk.END)
                self.text.insert('1.0', details)

            elif 'Remove' in opt:
                # Remove the selected amplifier
                self.control_system.remove_amplifier(serial_number)
                self.lb_files.delete(self.lb_files.curselection())

        self.lb_opt.bind('<Double-1>', selection)

    def list_all(self):
        amplifiers = self.control_system.list_amplifiers()
        self.lb_files.delete(0, tk.END) #clear

        for amplifier in amplifiers:
            self.lb_files.insert(tk.END, amplifier.serial_number)  # Add all amplifiers' serial numbers to the list

        if not amplifiers:
            self.lb_files.insert('1.0', "No amplifiers registered in the system.")

    def add_new_amplifier(self):
        """Prompt user for amplifier details and add it to the control system."""
        try:
            serial_number = simpledialog.askstring("Input", "Enter Serial Number:")
            model = simpledialog.askstring("Input", "Enter Model:")
            manufacturer = simpledialog.askstring("Input", "Enter Manufacturer:")
            next_maintenance = simpledialog.askstring("Input", "Enter Next Maintenance Date (DD-MM-YYYY):")
            sampling_rate = simpledialog.askinteger("Input", "Enter Sampling Rate (256, 512, 1024):")
            gain = simpledialog.askinteger("Input", "Enter Gain (1-100):")

            try:
                next_maintenance_date = datetime.strptime(next_maintenance, "%d-%m-%Y")
            except ValueError:
                messagebox.showerror("Invalid Date", "Date format should be YYYY-MM-DD")
                return

            # Create, add and include amplifier in list
            amplifier = Amplifier(serial_number=serial_number, model=model, manufacturer=manufacturer,
                                next_maintenance=next_maintenance_date, sampling_rate=sampling_rate, gain=gain)
            self.control_system.register_amplifier(amplifier)
            self.lb_files.insert(tk.END, serial_number)

        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def search_for_amplifier(self):
        result = create_search_dialog(self.root)

        if result['option'] == 'Manufacturer':
            sol = self.control_system.search_amplifier(manufacturer=result['string'])
        elif result['option'] == 'Serial number':
            sol = self.control_system.search_amplifier(serial_number=result['string'])
        elif result['option'] == 'Model':
            sol = self.control_system.search_amplifier(model=result['string'])

        self.lb_files.delete(tk.END)
        for amplifiers in sol:
                self.lb_files.insert(tk.END, amplifiers.serial_number)  # Add found amplifiers to the list      
        if not sol:
            self.lb_files.insert(tk.END, 'No matches found')

def main (args):
    root=tk.Tk()
    root.geometry("800x600")
    root.title("EEG Amplifier Control System")
    bapp = EEGAmplifier(root, args) 
    bapp.mainLoop()

if __name__ == "__main__":
   main(sys.argv)