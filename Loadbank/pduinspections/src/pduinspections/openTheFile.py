'''
The function to openFile on json
John Schuster
john.schuster1978@gmail.com
last edited 20220613 08:50 CDT.
'''
import json

def checkJsonFile(jsonFile, TextIn, WhatToDo, DictInfo):
    
    
    if WhatToDo == 'Update':
        if jsonFile == 'Hello World!':
            jsonFile = {TextIn:DictInfo}
            
        else:
            if TextIn in jsonFile:
                jsonFile[TextIn] = DictInfo
            if not TextIn in jsonFile:
                jsonFile.update({TextIn:DictInfo})
                
        return jsonFile
        
    if WhatToDo == 'Checking':
    
        if TextIn in jsonFile:
            
            return True

def openFile(fileLoc, RW, DataStuff):
    try:
        with open(fileLoc, RW, encoding="UTF-16")as f:
        
            match RW:
            
                case 'r':
                
                    try:
                        a = json.load(f)
                    except (IOError, ValueError):
                        a = 'Hello World!'
                    return a
                case 'r+':
                    try:
                        a=json.load(f)
                    except (IOError, ValueError):
                        a = "Hello World!"
                    return a
                case 'w':
                    json.dump(DataStuff, f, indent=4)
                case 'w+':
                    json.dump(DataStuff, f, indent=4)
                case 'a+':
                    json.dump(DataStuff, f, indent=4)
    except IOError:
        a = "Hello World!"
        return a