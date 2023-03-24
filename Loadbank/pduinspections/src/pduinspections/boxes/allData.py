import datetime
import toga
import ubelt as ub
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from ..DB.dbinterface import DBInterface
 

class DataStart:

    def __init__(self, homehandler, childhandler, errhandler):
        
        self.__Returnhandler = homehandler
        self.__Childhandler = childhandler
        self.__errhandler = errhandler
        self.choosenumber = 2
        self.pdunumbers = 47

    def Build(self):
        

        main_box = toga.Box()
        main_box.style.update(direction=COLUMN, padding_top=10, flex=1)

        
        main_box.add(self.__Build_RowOne())
        

        return main_box

    def __Build_RowOne(self):
        row1_box = toga.Box()
        row1_box.style.update(direction=ROW, padding_left=5, flex=1)

        row1_box.add(self.__Build_Label("Make Selection"))

        title_inputbox = toga.Box()
        title_inputbox.style.update(direction=ROW, alignment=RIGHT, padding_left=5, flex=1)
        
        title_inputbox.add(self.__Build_MenuItem('Single PDU.',self.__ActivateDataSingle))
        
        title_inputbox.add(self.__Build_MenuItem('Multiple PDUs.',self.__ActivateDataMulti))
        
        
        

        row1_box.add(title_inputbox)

        return row1_box



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

        
        menubox.add(self.__Build_MenuItem("Submit",self.__Return))
        menubox.add(self.__Build_MenuItem("Return Home",self.__Return))

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
        self.__Childhandler(whichWindow)
        
    def __ActivateDataSingle(self, widget):
        data = {'PDUNumbers': 2}
        depends = 'repr-of-params-that-uniquely-determine-the-process'
        #Create a cacher and try loading the data

        cacher = ub.Cacher('PDUNumber' , depends, verbose=4)
        cacher.save(data)
        assert cacher.exists(), 'should now exist'
        self.__Childhandler("DataEnter")
        
    def __ActivateDataMulti(self, widget):
        
        data = {'PDUNumbers': 7}
        depends = 'repr-of-params-that-uniquely-determine-the-process'
        #Create a cacher and try loading the data

        cacher = ub.Cacher('PDUNumber' , depends, verbose=4)
        cacher.save(data)
        assert cacher.exists(), 'should now exist'
        self.__Childhandler("DataEnter")
        
        
        
class DataEnter:

    def __init__(self, homehandler, childhandler, errhandler, dataStartbox):
        
        data = []
        self.__Returnhandler = homehandler
        self.__Childhandler = childhandler
        self.__errhandler = errhandler
        depends = 'repr-of-params-that-uniquely-determine-the-process'
        cacher = ub.Cacher('PDUNumber', depends, verbose=4)
        data= cacher.tryload()
        self.__pdunumbers = data['PDUNumbers'] - 1
        del cacher
        
        self.__pdudata = {}
        self.__pduserial =[1,2,3,4,5,6]
        self.__pdumodel = [1,2,3,4,5,6]

    def Build(self):
        
        
        main_box = toga.Box()
        main_box.style.update(direction=COLUMN, padding_top=10, flex=1)
        
        match self.__pdunumbers:
        
            case 1:
                main_box.add(self.__Build_RowOne(1))
                
            case 6:
                #add loop here to do __Build_RowOne with 1 or 6 spots
                for i in range(0,self.__pdunumbers):
                    main_box.add(self.__Build_RowOne(i))
            case _:
                main_box.add(self.__Build_Label(f'{self.__pdunumbers}'))

        main_box.add(self.__Build_Chooser())

        return main_box

    def __Build_RowOne(self, i):
        row1_box = toga.Box()
        row1_box.style.update(direction=COLUMN, padding_left=5, flex=1)
        
        serial_model_box = toga.Box()
        serial_model_box.style.update(direction = ROW, padding_left=5, flex = 1)
        
    
        row1_box.add(self.__Build_Label(f"Enter Serial Number and Model Number for PDU {i+1}"))
        #use a dict to gather all the data.
        self.__pduserial[i] = toga.TextInput(style=Pack(width=150, alignment=RIGHT, padding=(0,2), flex=1))
        self.__pdumodel[i] = toga.TextInput(style=Pack(width=150, alignment=RIGHT, padding=(0,2), flex=1))
        serial_model_box.add(self.__pduserial[i])
        serial_model_box.add(self.__pdumodel[i] )
        
        row1_box.add(serial_model_box)

        return row1_box



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

        menubox.add(self.__Build_MenuItem("Add Player",self.__ActivateChild))
        menubox.add(self.__Build_MenuItem("Submit",self.__Return))
        menubox.add(self.__Build_MenuItem("Return Home",self.__Return))

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

    def __ActivateChild(self, whichWindow):
        self.__Childhandler(whichWindow)
        
    def __ActivateSingle(self, widget):
        self.__Childhandler("SingleData")