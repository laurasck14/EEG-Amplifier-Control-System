#!/usr/bin/env python3
''' Laura Santa Cruz Kaster
usage: python3 gui.py
'''
import sys, os, re
import tkinter as tk
import tkinter.ttk as ttk
from GuiBaseClass import GuiBaseClass
import tkinter.filedialog as filedialog
import Amplifier as amplifier

class EEGAmplifier(GuiBaseClass):
    def __init__(self, root, args):
        super().__init__(root)
    
        mnu=self.getMenu('Search')

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