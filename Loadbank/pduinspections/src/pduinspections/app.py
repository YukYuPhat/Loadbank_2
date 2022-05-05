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

        self.main_window = toga.MainWindow(title=self.formal_name)

        Display = BoxManager(self.main_window)
        Display.BuildBoxes()

def main():
    return TennisLeague()