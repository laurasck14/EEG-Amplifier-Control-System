import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as mbox
import sys
class GuiBaseClass():
  def __init__(self,root):
      # create widgets
      self.root=root
      self.root.option_add('*tearOff', False)
      self.menu=dict()
      self.menubar = tk.Menu(root)         
      menu_file = tk.Menu(self.menubar)
      self.menubar.add_cascade(menu=menu_file,label='File',underline=0)
      menu_file.add_separator()
      menu_file.add_command(label='Exit', 
          command=self.Exit,underline=1)           
      menu_help = tk.Menu(self.menubar)
      self.menubar.add_cascade(menu=menu_help,label='Help',underline=0)
      menu_help.add_command(label='About', command=self.About,underline=0)       
      root.config(menu=self.menubar)
      self.menu['menubar'] = self.menubar
      self.menu['File']    = menu_file        
      self.menu['Help']    = menu_help              
      self.frame = ttk.Frame(root)
      self.frame.pack(fill='both',expand=True)

  # public functions
  def mainLoop(self):
      self.root.mainloop()

  def getFrame(self):
      return(self.frame)  
  
  def getMenu(self,entry):
      if entry in self.menu:
        return (self.menu[entry])
      else:
        # we create a new one
        last = self.menu['menubar'].index('end')   
        self.menu[entry]= tk.Menu(self.menubar)
        self.menu['menubar'].insert_cascade(
          last, menu=self.menu[entry],label=entry)
        return(self.menu[entry])
  # private functions
  def Exit(self,ask=True):
      res = mbox.askyesno(title="Are you sure?",message="Really quit the application?")
      if res:
          sys.exit(0)
          
  def About(self):
    text_window = tk.Toplevel()
    text_window.title("Help page")

    text = """USAGE: python3 gui.py coded by Laura Santa Cruz
      EEG Amplifier Control system GUI allows to modify, search, delete, add amplifiers.

      Left box: list of the currently registered amplifiers
      Middle menu: optional operations to perform to a selected amplifier
        - must select an amplifier AND double click on the option
      Right box: output of the results"""

    text_window.geometry("1000x250")
    # Add a Text widget to the window to display the text content
    text_display = tk.Text(text_window, wrap='word')
    text_display.insert(tk.END, text)  # Insert the text content
    text_display.config(state='disabled')  # Make the Text widget read-only
    text_display.pack(expand=True, fill='both')
    
if __name__ == '__main__':
    root=tk.Tk()
    bapp = GuiBaseClass(root) 
    # example for using the BaseClass in other applications
    mnu=bapp.getMenu('Edit')
    mnu.add_command(label='Copy',command=lambda: print('Copy'))    
    # example for using getFrame
    frm=bapp.getFrame()
    btn=ttk.Button(frm,text="Button X",command=lambda: sys.exit(0))
    btn.pack()
    bapp.mainLoop()