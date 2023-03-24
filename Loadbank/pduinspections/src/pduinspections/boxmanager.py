import toga
import ubelt as ub
from toga.style import Pack
from toga.style.pack import COLUMN, ROW, LEFT, RIGHT
#below are the imported classes from files.py
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
        '''
        This return home is what is used to get back to the main menu.  use rebuild variable to get data returned from the other file.  
        '''
        depends = 'repr-of-params-that-uniquely-determine-the-process'
        cacher = ub.Cacher('LocationData', depends, verbose=4)
        data = cacher.tryload()
        if data is None or rebuild == "Clear":
            #starts the main menu from scratch
            self.__location = 'Bob' 
        else:
            #adds location data to the main menu
            self.__location = data
            
        
        #sends you back to the home screen
        if rebuild == True or rebuild == 'Clear':
            
            # this builds the main menu by calling  self.__BuildHomeBox
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
    
    #this sets up all the other pages of the program  
        self.__RootBox.style.update(direction=ROW)

        '''
        
        #build dataenter box to call when needed. this is from the allData.py file
        dataEnterBox = DataEnter(self.ReturnHome, self.ActivateBox, self.__ErrorHandler, self.__howmany)  # this is the class called from another file.py
        self.__d_Boxes["DataEnter"] = dataEnterBox.Build() #calls the build function and adds it to the dictionary under "DataCenter"
        
        
        
        '''
        

        

        #build the which location box, SetLocationStuff.py is the file.
        whichLoc = WhichLocation(self.ReturnHome, self.ActivateBox, self.__ErrorHandler)
        self.__d_Boxes["WhichLocation"] = whichLoc.Build()
        self.whichList = whichLoc.list_stuff 
        
        #build datastart box to call when needed. this is from the allData.py file
        dataStartbox = DataStart(self.ReturnHome, self.ActivateBox, self.__ErrorHandler)
        self.__d_Boxes["DataStart"] = dataStartbox.Build()
        
        
        
        #build dataenter box to call when needed. this is from the allData.py file
        dataEnterBox = DataEnter(self.ReturnHome, self.ActivateBox, self.__ErrorHandler, dataStartbox)
        self.__d_Boxes["DataEnter"] = dataEnterBox.Build()

#        newplayer = NewPlayer(self.__database, self.ReturnLast, self.__ErrorHandler)
#        self.__d_Boxes["NewPlayer"] = newplayer.Build()
        
        #build the home box and add buttons.  change __BuildHomeBox to affect this
        self.__d_Boxes["HomeBox"] = self.__BuildHomeBox()
        self.__RootBox.add(self.__d_Boxes["HomeBox"])
        
        self.__MainWindow.content = self.__RootBox # gets mainwindow from the app.py file
        self.__MainWindow.show() #show the main window

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
        self.__handler = handler # this is the dictonary of all the sub windows/boxes
        #build the main menu box
        self.__RootBox = toga.Box() #calls toga.Box for the base of the app
        
        self.__whichPDU = location #This is data from the selection.
        stuffBox = [] #not used yet.

    def Build(self):
        # update the root box 
        self.__RootBox.style.update(direction=COLUMN, alignment=LEFT) 

        locationbox = toga.Box() #building the new box 
        locationbox.style.update(direction=ROW, alignment=RIGHT)# updates the style
        # The first button to get location
        locationbox.add(self.__Build_MenuItem("Input Location",self.show_input_window)) #use Build_MenuItem function to build buttons
        
        

        self.__RootBox.add(locationbox) # add the above box to root
        locationlabelbox = toga.Box() # building the label for the box above.
        
       
        
        
        # leaves a blank below the button    
        if self.__whichPDU == '':    
        
            locationlabelbox.add(self.__Build_MenuLabel(self.__whichPDU)) 
            
        # Gives location on front page
        if not self.__whichPDU == '':
             
            buildingText = f'Building: {self.__whichPDU["Building"]}'
            locationlabelbox.add(self.__Build_MenuLabel(buildingText))
            ColoText = f'COLO: {self.__whichPDU["COLO"]}'
            locationlabelbox.add(self.__Build_MenuLabel(ColoText))
            CellText = f'Cell: {self.__whichPDU["CE"]}'
            locationlabelbox.add(self.__Build_MenuLabel(CellText))
            PDUText = f'PDU: {self.__whichPDU["PDU Name"]}'
            locationlabelbox.add(self.__Build_MenuLabel(PDUText))
            locationlabelbox.style.update(direction=COLUMN, alignment=RIGHT)
            
            self.__RootBox.add(locationlabelbox)
            stuffBox = {}
            for things in ['Data']:
                
                match things:
                
                    case 'Data':
                        stuffBox[f'{things}'] = toga.Box()
                        stuffBox[f'{things}'].style.update(direction=ROW, alignment=RIGHT)
                        # The first button to get location
                        stuffBox[f'{things}'].add(self.__Build_MenuItem(f"{things}",self.show_data_window))
                        self.__RootBox.add(stuffBox[f'{things}'])
        

        self.__RootBox.add(locationbox) #it always takes this box.
                
        return self.__RootBox #returns it to the call

# todo: make this function more generic so it can take multiple handlers.
    def show_input_window(self, widget): # use this in the __Build_MenuItem function.  This is what is called when button pushed.
        self.__handler("WhichLocation") #is used to call the specific page in the app
        
    def show_data_window(self, widget):# use this in the __Build_MenuItem function.  This is what is called when button pushed.

        self.__handler("DataStart")  #is used to call the specific page in the app

    def new_player_window(self, widget):# use this in the __Build_MenuItem function.  This is what is called when button pushed.
        self.__handler("NewPlayer") #is used to call the specific page in the app

    def __Build_MenuItem(self, label, action): # this function is called to build a button
        itembox = toga.Box()
        itembox.style.update(direction=ROW)


        button = toga.Button(
            label,
            on_press=action,
            style=Pack(padding=5)
        )
        itembox.add(button)

        return itembox
        
    def __Build_MenuLabel(self, label): # this function is used to build a label.
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
