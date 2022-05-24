'''
The function to openFile on json
John Schuster
john.schuster1978@gmail.com

'''
import json


def openFile(fileLoc, RW,DataStuff):
    try:
        with open(fileLoc, RW)as f:
        
            match RW:
                case 'r+':
                    try:
                        a=json.load(f)
                    except (IOError, ValueError):
                        a = "Hello World!"
                    return a
                case 'w+':
                    json.dump(DataStuff, f, indent=4)
                case 'a+':
                    json.dump(DataStuff, f, indent=4)
    except IOError:
        a = "Hello World!"
        return a