# EEG-Amplifier-Control-System
EEG Amplifier Control System consists of a GUI to manage amplifiers. It allows the user to create a new one, delete a selected one and search based on serial number, model or manufacturer. Gain, sample rate and power can also be modified.

The implementation for exporting the current data into a file was started but not finished.

## Includes:
  - Amplifier.py: where the class for the amplifier and sensor is
  - gui.py: GUI display and functions
  - two_input.py: combobox designed to accept two inputs from the user
  - GuiBaseClass.py: frame for the gui.py

*usage:* python3 gui.py
