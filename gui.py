#!/usr/bin/env python3
''' Laura Santa Cruz Kaster
USAGE: python3 gui.py
EEG Amplifier Control system GUI allows to modify, search, delete, add amplifiers.

Left box: list of the currently registered amplifiers
Middle menu: optional operations to perform to a selected amplifier
    - must select an amplifier AND double click on the option
Right box: output of the results
'''

import sys, os, re
import tkinter as tk
import tkinter.ttk as ttk
from GuiBaseClass import GuiBaseClass
from tkinter import simpledialog, messagebox, filedialog
from Amplifier import EEGAmplifierControlSystem, Amplifier, Sensor
from datetime import datetime
from two_input import create_search_dialog
import json


class EEGAmplifier(GuiBaseClass):
    def __init__(self, root, args):
        super().__init__(root)
        self.control_system = EEGAmplifierControlSystem()

        mnu=self.getMenu('Import/export data')
        #mnu.add_command(label='Save amplifiers', command=self.save_to_file)

        mnu=self.getMenu('Amplifier')
        mnu.add_command(label='List all', command=self.list_all)
        mnu.add_command(label='Add new amplifier', command=self.add_new_amplifier)
        mnu.add_command(label='Search amplifier', command=self.search_for_amplifier)

        mf = self.getFrame()
        self.pw = ttk.PanedWindow(mf, orient='horizontal')

        self.lb_files = tk.Listbox(self.pw, exportselection=True)
        self.lb_opt = tk.Listbox(self.pw, exportselection=False)
        self.pw.add(self.lb_files)
        self.lb_opt.insert(1,'Information') #middle menu options
        self.lb_opt.insert(2,'Remove')
        self.lb_opt.insert(3,'Set gain')
        self.lb_opt.insert(4,'Set sample rate')
        self.lb_opt.insert(5,'Set power')
        self.lb_opt.insert(6,'Add sensor')

        self.pw.add(self.lb_opt)

        self.text = tk.Text(self.pw, wrap='word',undo=True)
        self.pw.add(self.text)
        self.pw.pack(side='top', fill='both', expand=True)

        # functions from the middle menu, user must double click
        def selection(event):
            if not self.lb_files.curselection():
                self.text.insert(tk.END, "Please select an amplifier and double click on the option.\n")
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
                self.text.insert(tk.END, f'\nAmplifier {serial_number} deleted\n')

            elif 'Set gain' in opt:
                new_gain = simpledialog.askinteger("Modify Gain", "Select an amplifier and enter new gain value (1-100):", minvalue=1, maxvalue=100)
                if new_gain is not None:
                    try:
                    # Set the gain for the selected amplifier
                        amplifier.set_gain(new_gain)
                        self.text.delete('1.0', tk.END)
                        self.text.insert(tk.END, f'\nGain modified for amplifier {amplifier.serial_number}.\n')

                    except ValueError as e:
                        self.text.delete('1.0', tk.END)
                        self.text.insert(tk.END, e)
           
            elif 'Set sample rate' in opt:
                new_rate = simpledialog.askinteger("Modify sampling rate", "Select an amplifier and enter new sampling rate [256, 512, 1024]:")
                if new_rate is not None:
                    try:
                    # Set the sample rate for the selected amplifier
                        amplifier.set_sampling_rate(new_rate)
                        self.text.delete('1.0', tk.END)
                        self.text.insert(tk.END, f'\nSample rate modified for amplifier {amplifier.serial_number}\n')

                    except ValueError as e:
                        self.text.insert(tk.END, e)


            elif 'Set power' in opt:
                amplifier.toggle_power()
                self.text.delete('1.0', tk.END)                
                self.text.insert(tk.END, f'\nPower modified for {amplifier.serial_number}.\n')

            elif 'Add sensor' in opt:
                # Prompt the user to enter sensor tag
                sensor_tag = simpledialog.askstring("Add Sensor", "Enter sensor tag (e.g., 'frontal', 'occipital'):")
                if sensor_tag:
                    new_sensor = Sensor(tag=sensor_tag)
                    amplifier.add_sensor(new_sensor)
                    self.text.delete('1.0', tk.END)  
                    self.text.insert(tk.END, f"\nSensor '{sensor_tag}' added to amplifier {amplifier.serial_number}.\n")

        self.lb_opt.bind('<Double-1>', selection)
    
    # Start of the implementation to save amplifiers created into a file, not working
    # def save_to_file(self):
    #     file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
    #     if file_path:
    #         data = [amplifier.to_dict() for amplifier in self.amplifiers]

    #     with open(file_path, 'w') as file:
    #         json.dump(data, file, indent=4)


    def list_all(self): # return all currently available amplifiers
        amplifiers = self.control_system.list_amplifiers()
        self.text.delete("1.0", tk.END)
        self.lb_files.delete(0, tk.END) #clear

        for amplifier in amplifiers:
            self.lb_files.insert(tk.END, amplifier.serial_number)  # Add all amplifiers' serial numbers to the list

        if not amplifiers:
            self.text.insert(tk.END, "No amplifiers registered in the system.\n")

    def add_new_amplifier(self): #register new amplifier
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
            self.text.delete("1.0", tk.END)
            self.text.insert(tk.END, '\nNew amplifier added.\n')

        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    def search_for_amplifier(self): #search for amplifier
        result = create_search_dialog(self.root) #open custom window to ask for input
        if result['option'] == 'Manufacturer':
            sol = self.control_system.search_amplifier(manufacturer=result['string'])
        elif result['option'] == 'Serial number':
            sol = self.control_system.search_amplifier(serial_number=result['string'])
        elif result['option'] == 'Model':
            sol = self.control_system.search_amplifier(model=result['string'])

        self.lb_files.delete(0, tk.END) #clear
        self.text.delete("1.0", tk.END)
        for amplifiers in sol:
                self.lb_files.insert(tk.END, amplifiers.serial_number)  # Add found amplifiers to the list 
        if not sol:
            self.text.insert(tk.END, '\nNo matches found\n')

def main (args): #generate main window
    root=tk.Tk()
    root.geometry("800x400")
    root.title("EEG Amplifier Control System")
    bapp = EEGAmplifier(root, args) 
    bapp.mainLoop()

if __name__ == "__main__":
   main(sys.argv)