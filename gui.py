#!/usr/bin/env python3
''' Laura Santa Cruz Kaster
usage: python3 LauraSantaCruzUniProtParser3.py
'''
import sys, os, re
import tkinter as tk
import tkinter.ttk as ttk
from GuiBaseClass import GuiBaseClass
import tkinter.filedialog as filedialog
import Amplifier as Amplifier

# usage: python3 gui.py

class EEGAmplifier(GuiBaseClass):
    def __init__(self,root,dirname,args):
        super().__init__(root)
        mnu=self.getMenu('File')
        mnu.insert_command(0, label='Open dir...', command=self.fileOpen)
       
        mf = self.getFrame()
        self.pw = ttk.PanedWindow(mf, orient='horizontal')
        self.lb_files = tk.Listbox(self.pw,exportselection=True)
        self.lb_opt = tk.Listbox(self.pw,exportselection=False)
        self.pw.add(self.lb_files)
        self.lb_opt.insert(1,'GO')
        self.lb_opt.insert(2,'KEGG')
        self.lb_opt.insert(3,'DOI')        
        self.pw.add(self.lb_opt)

        self.text = tk.Text(self.pw, wrap='word',undo=True)
        self.pw.add(self.text)
        self.pw.pack(side='top', fill='both', expand=True)

        def selection(event):
            if not self.lb_files.curselection():
                self.message("Please select a file")

            elif self.lb_files.curselection():
                filename = self.lb_files.get(self.lb_files.curselection())
                opt = self.lb_opt.get(self.lb_opt.curselection())
                #print('file:',filename,'\n command:',opt)

                # if 'GO' in opt:
                #     sol = Amplifier.get_go_ids(filename)
                #     self.text.insert('1.0',sol)
                    

        self.lb_opt.bind('<Double-1>', selection)

        # open filedialog in case no dirname is given and see the files in the directory if given
        self.dirname = dirname
        if (dirname == "" or dirname == "-"):
            self.fileOpen()
        else:
            dirname = args[1]
            all_files = os.listdir(dirname)
            self.message("Directory searched: "+ os.path.basename(dirname))
            for filename in all_files:
                self.lb_files.insert('end',filename)

    def fileOpen (self,dirname=''):
        if dirname == "" or not(os.path.exists(dirname)):
            dirname=filedialog.askdirectory(
                title='Select a directory',
                initialdir=os.path.dirname(self.dirname))
            all_files = os.listdir(dirname)        

        if dirname != "":
            for filename in all_files:
                #self.lb_files.insert('end',filename)
                self.message("Directory searched: "+ os.path.basename(dirname))
               
                # We only include in the display the files that end in .dat or .dat.gz
                if re.search('.+(dat|dat.gz$)',filename):
                    self.lb_files.insert('end',filename)

def main (args):
    # if no filename is provided we open the gui app and the option to give a filename
    if len(args) == 1:
        dirname=''
        root=tk.Tk()
        root.geometry("700x500")
        root.title("EEG Amplifier Control System")
        bapp = EEGAmplifier(root,dirname,args) 
        bapp.mainLoop()

    if len(args) > 1:
        dirname= args[1]
        root=tk.Tk()
        root.geometry("700x500")
        root.title("EEG Amplifier Control System")
        bapp = EEGAmplifier(root,dirname,args) 
        bapp.mainLoop()

if __name__ == "__main__":
   main(sys.argv)