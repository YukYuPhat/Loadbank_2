"""
PDU Inspections for ABB at Microsoft.
"""
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from pduinspections import BoxManager

class PDUInspections(toga.App):

    def startup(self):
        """
        Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        #build the main window to pass to boxmanager
        self.main_window = toga.MainWindow(title=self.formal_name)
        
        #calling BoxManager Class and passing the main window.
        Display = BoxManager(self.main_window)
        
        #call the base function in BoxManager 
        Display.BuildBoxes()

def main():
    return PDUInspections()