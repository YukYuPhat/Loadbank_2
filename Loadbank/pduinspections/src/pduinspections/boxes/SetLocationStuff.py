import datetime
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from ..DB.dbinterface import DBInterface
from ..DB.openTheFile import openFile


class WhichLocation:

    def __init__(self, homehandler, childhandler, errhandler):
        
        self.__Returnhandler = homehandler
        self.__Childhandler = childhandler
        self.__errhandler = errhandler
        self.__locationList = ['COLO','CE','PDU'] 
        self.ColoLoc = ''
        self.PDULoc = ''
        self.CELoc = ''
        self.list_stuff = ['0','0','0']

    def Build(self):
        

        main_box = toga.Box()
        main_box.style.update(direction=COLUMN, padding_top=10, flex=1)

        
        main_box.add(self.__Build_RowOne(self.__locationList[0]))
        main_box.add(self.__Build_RowTwo(self.__locationList[1]))
        main_box.add(self.__Build_RowThree(self.__locationList[2]))
        main_box.add(self.__Build_Chooser())

        return main_box

    def __Build_RowOne(self, stuff):
        row1_box = toga.Box()
        row1_box.style.update(direction=ROW, padding_left=5, flex=1)

        row1_box.add(self.__Build_Label(f"What {stuff} are you in?"))

        title_inputbox = toga.Box()
        title_inputbox.style.update(direction=COLUMN, alignment=RIGHT, padding_left=5, flex=1)
        self.__title_input1 = toga.TextInput(style=Pack(width=150, alignment=RIGHT, padding=(0,2), flex=1))
        title_inputbox.add(self.__title_input)
        self.coloStart = self.__title_input.value1
        row1_box.add(title_inputbox)

        return row1_box

    def __Build_RowTwo(self, stuff):
        row2_box = toga.Box()
        row2_box.style.update(direction=ROW, padding_left=5, padding_top=10, flex=1)

        row2_box.add(self.__Build_Label(f"What {stuff} are you in?"))

        title_inputbox = toga.Box()
        title_inputbox.style.update(direction=COLUMN, alignment=RIGHT, padding_left=5, flex=1)
        self.__title_input2 = toga.TextInput(style=Pack(width=150, alignment=RIGHT, padding=(0,2), flex=1))
        self.cellStart = self.__title_input.value2
        title_inputbox.add(self.__title_input)

        row2_box.add(title_inputbox)

        return row2_box
        
    def __Build_RowThree(self, stuff):
        row3_box = toga.Box()
        row3_box.style.update(direction=ROW, padding_left=5, padding_top=10, flex=1)

        row3_box.add(self.__Build_Label(f"What {stuff} are you in?"))

        title_inputbox = toga.Box()
        title_inputbox.style.update(direction=COLUMN, alignment=RIGHT, padding_left=5, flex=1)
        self.__title_input3 = toga.TextInput(style=Pack(width=150, alignment=RIGHT, padding=(0,2), flex=1))
        self.pduStart = self.__title_input.value3
        title_inputbox.add(self.__title_input)

        row3_box.add(title_inputbox)

        return row3_box        

    def __Build_Label(self, text):
        label_box = toga.Box()
        label_box.style.update(direction=ROW)
        label_name = toga.Label(text)
        label_box.add(label_name)

        return label_box

    def __Build_Chooser(self):
        main_box = toga.Box()
        main_box.style.update(direction=ROW,flex=1)

        menubox = toga.Box()
        menubox.style.update(direction=ROW,padding_left=10,flex=1)
        
        

        menubox.add(self.__Build_MenuItem("Submit",self.__ActivateChild))
        menubox.add(self.__Build_MenuItem("Return Home without location.",self.__Return))

        main_box.add(menubox)



        return main_box

    def __Build_MenuItem(self, label, action):
        itembox = toga.Box()
        itembox.style.update(direction=ROW)

        button = toga.Button(
            label,
            on_press=action,
            style=Pack(padding=5)
        )
        itembox.add(button)

        return itembox

    def __Return(self, widget):
        self.__Returnhandler()

    def __ActivateChild(self, widget):
        
        data = {'COLO': self.coloStart, 'CE':self.cellStart, 'PDU Name':self.cellStart}
        openFile('cacheData.json', 'w', data)
        
        self.__Returnhandler(True)
        
    