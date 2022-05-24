import sqlite3
import re
import os

dirname = os.path.dirname(__file__)
s_DB = os.path.join(dirname, "PDU_Database.db")
#s_Sheet = os.path.join(dirname, "PDU_Example.xlsx")

class DBInterface:

    def __init__(self):
        #sql objects
        self.__conn = sqlite3.connect(s_DB)
        self.__cursor = self.__conn.cursor()
        
        self.__table_List = [r'pdu',r'amperage',r'epms',r'voltage']
        self.__pdu_cols = [r'name',r'model number',r'serial number',r'color']
        self.__epms_cols = [r'IP',r'Gateway',r'Subnet',r'Modbus1',r'Modbus2',
                    r'Enable2Wire',r'BaudRate',r'EnableRTU',r'EnableTCP',r'Timezone',
                    r'Time_Date',r'MCB',r'Excess_Sensor',r'OverTemp_sensor',r'MCBTrips',
                    r'LowArc',r'FB1',r'FB2',r'FB3',r'FB4',
                    r'PIBa',r'PIBb',r'PIBc',r'FB1A',r'FB1B',
                    r'FB1C',r'FB1N',r'FB2A',r'FB2B',r'FB2C',
                    r'FB2N',r'FB3A',r'FB3B',r'FB3C',r'FB3N',
                    r'FB4A',r'FB4B',r'FB4C',r'FB4N',r'pdu_id']

        #excel objects
#        self.__wb = openpyxl.load_workbook(filename = s_Sheet)
#        self.__ws = self.__wb.active

        #if I ever build a 'new sheet' function I need to look at setting these better
#        self.__s_StartCol = "J"
#        self.__s_EndCol = "BA"

#SQL Queries

    def get_PDUdict(self): #fix
        query = "SELECT name FROM pdu"
        self.__cursor.execute(query)

        return dict(tuple(self.__cursor.fetchall()))

    # this returns a specific column in the table.  look to init module. returns one column in table only.
    def get_PDUnames(self, col_List, table):  
        query = f"SELECT {col_List} FROM {table}"
        self.__cursor.execute(query)

        return self.__cursor.fetchall()

    def get_nums(self):#fix
        query = """SELECT Name, Number
            FROM Players ORDER BY Number DESC"""
        self.__cursor.execute(query)

        return self.__cursor.fetchall()

#SQL Updates

    def __insert_num(self, querydata):#fix
        query = """UPDATE Players set Number = (?)
                WHERE Name = (?)"""

        self.__cursor.execute(query, querydata)
        self.__conn.commit()

        return 1
    
    def __insert_updates(self, table, col_List, value_Stuff):
        query = f'''UPDATE {table} ({col_List}) = ({value_Stuff})'''
        try:
            self.__cursor.execute(query)
            self.__conn.commit()  
        except Error as e:
            print(f"The error '{e}' occurred")
        return 1