import toga
import ubelt as ub
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
from .DB.dbinterface import DBInterface
from .boxes.errorbox import ErrorBox
from .boxes.SetLocationStuff import WhichLocation
from .boxes.allData import DataStart
from .boxes.allData import DataEnter
from .DB.openTheFile import openFile
from .DB.openTheFile import checkJsonFile


class BoxManager:

    def __init__(self, mainwindow):
        
        #gets mainwindow from app.py when calling the class.
        self.__MainWindow = mainwindow
        
        #making the root box everything goes into.
        self.__RootBox = toga.Box()
        
        #calls the error box and brings it to this file
        self.__ErrBox = ErrorBox(self.ActivateBox)
        
        #builds the Current Box and sets it to Homebox
        self.__ActiveBox = "HomeBox"
        
        #builds the Home Box and sets it to Homebox
        self.__HomeBox = "HomeBox"
        
        #builds the Last Box and sets it to Homebox
        self.__LastBox = "HomeBox"
        
        #builds the dict for all the boxes to be put into and called from
        self.__d_Boxes = dict()
        
        #works the data base and what is needed from there.
        self.__database = DBInterface()
        
        #location list
        self.__location = ''
        
        #for data entry on how many pdus to work data.
        self.__howmany = 0

    def ReturnHome(self, rebuild):
        depends = 'repr-of-params-that-uniquely-determine-the-process'
        cacher = ub.Cacher('LocationData', depends, verbose=4)
        data = cacher.tryload()
        if data is None or rebuild == "Clear":
        
            self.__location = ''
        else:
            self.__location = data
        
        #sends you back to the home screen
        if rebuild == True or rebuild == 'Clear':
            
            self.__d_Boxes["HomeBox"] = self.__BuildHomeBox()
            
        #removes/closes current box/screen
        self.__RootBox.remove(self.__d_Boxes[self.__ActiveBox])
        
        #add home box to root.
        self.__RootBox.add(self.__d_Boxes[self.__HomeBox])
        
        #sets closing box to last
        self.__LastBox = self.__ActiveBox
        
        #sets Active box to Homebox
        self.__ActiveBox = "HomeBox"

    def ReturnLast(self):
        self.__RootBox.remove(self.__d_Boxes[self.__ActiveBox])
        self.__RootBox.add(self.__d_Boxes[self.__LastBox])
        savelast = self.__LastBox
        self.__LastBox = self.__ActiveBox
        self.__ActiveBox = savelast

    def ActivateBox(self, boxname):
        self.__RootBox.remove(self.__d_Boxes[self.__ActiveBox])
        self.__RootBox.add(self.__d_Boxes[boxname])
        self.__LastBox = self.__ActiveBox
        self.__ActiveBox = boxname

    def __BuildHomeBox(self):
        
        
        #don't need to add anything to this.  only need main menu.
        #build the root box
        root = toga.Box()
        root.style.update(direction=ROW,flex=1)
        

        #Build a first box, but not needed.
#        rankobj = Rankings(playerinfo)
#        rankbox = rankobj.Build()
        
        menuobj = MainMenu(self.ActivateBox, self.__location)
        menubox = menuobj.Build()
        
#        root.add(rankbox)
        root.add(menubox)

        return root

    def BuildBoxes(self):
        self.__RootBox.style.update(direction=ROW)

#        d_Players = self.__database.get_playerdict()
        

        
        #build datastart box to call when needed. this is from the allData.py file
        dataStartbox = DataStart(self.ReturnHome, self.ActivateBox, self.__ErrorHandler)
        self.__d_Boxes["DataStart"] = dataStartbox.Build()
        self.__howmany = dataStartbox.choosenumber
        
        #build dataenter box to call when needed. this is from the allData.py file
        dataEnterBox = DataEnter(self.ReturnHome, self.ActivateBox, self.__ErrorHandler, self.__location, self.__howmany)
        self.__d_Boxes["DataEnter"] = dataEnterBox.Build()

        #build the which location box, SetLocationStuff.py is the file.
        whichLoc = WhichLocation(self.ReturnHome, self.ActivateBox, self.__ErrorHandler)
        self.__d_Boxes["WhichLocation"] = whichLoc.Build()
        self.whichList = whichLoc.list_stuff 
        
#        newplayer = NewPlayer(self.__database, self.ReturnLast, self.__ErrorHandler)
#        self.__d_Boxes["NewPlayer"] = newplayer.Build()
        
        #build the home box and add buttons.  change __BuildHomeBox to affect this
        self.__d_Boxes["HomeBox"] = self.__BuildHomeBox()
        self.__RootBox.add(self.__d_Boxes["HomeBox"])

        self.__MainWindow.content = self.__RootBox
        self.__MainWindow.show()

    def __ErrorHandler(self,errmsg="Unknown Error",fatalflg=False,returnwin="HomeBox"):
        if fatalflg == True:
            self.__d_Boxes["ErrorBox"] = self.__ErrBox.Build(errmsg, returnwin)
            self.ActivateBox("ErrorBox")
        else:
            self.__MainWindow.info_dialog(
                'Error:',
                errmsg
            )
   
class MainMenu:
    
    def __init__(self, handler, location):
        self.__handler = handler
        #build the main menu box
        self.__RootBox = toga.Box()
        
        self.__whichPDU = location

    def Build(self):
        # update the root box 
        self.__RootBox.style.update(direction=COLUMN, alignment=LEFT)

        locationbox = toga.Box()
        locationbox.style.update(direction=ROW, alignment=RIGHT)
        
        locationbox.add(self.__Build_MenuItem("Input Location",self.show_input_window))
        
        

        self.__RootBox.add(locationbox)
        locationlabelbox = toga.Box()
        
       
        
        
            
        if self.__whichPDU == '':    
        
            locationlabelbox.add(self.__Build_MenuLabel(self.__whichPDU))
            
        
        if not self.__whichPDU == '':
             
            
            locationlabelbox.add(self.__Build_MenuLabel(self.__whichPDU))
            
        self.__RootBox.add(locationlabelbox)
        return self.__RootBox

# todo: make this function more generic so it can take multiple handlers.
    def show_input_window(self, widget):
        self.__handler("WhichLocation")
        
    def new_season_window(self, widget):
        self.__handler("NewSeason")

    def new_player_window(self, widget):
        self.__handler("NewPlayer")

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
        
    def __Build_MenuLabel(self, label):
        labelbox = toga.Box()
        labelbox.style.update(direction=ROW)
        
        labelStuff = toga.Label(label)
        
        labelbox.add(labelStuff)
        
        return labelbox

    def is_list_empty(self,list):
        # checking the length
        if len(list) == 0:
            # returning true as length is 0
            return True
        # returning false as length is greater than 0
        return False
