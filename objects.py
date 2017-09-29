'''
Created on Sep 25, 2017

@author: rclaus
'''
import quickstep as q

class Table:
    def __init__(self,name,columns):
        self.columns=columns
        self.name=name
    
    def size(self):
        return tableSize(self.name)
        
    def copyReference(self):
        return Table(self.name,self.columns)
    
    def toString(self):
        return printTable(self.name)
        
        
class Literal:
    def __init__(self,table,columns,columnMapping):
        self.name=table
        self.columnMapping=columnMapping
        self.columns=columns
        self.score=-1
        
    def setScore(self,score):
        self.score=score
        
    def getScore(self):
        return self.score
    
    def size(self):
        return tableSize(self.name)
    
    def copyReference(self):
        return Literal(self.name,self.columns,self.columnMapping)
    
    
    def toString(self):
        return printTable(self.name)
    
def tableSize(tableName):
    return int(q.sql_to_table("SELECT COUNT(*) AS c FROM "+tableName).iloc[0]['c'])

def printTable(name):
    return q.sql_to_table("SELECT * FROM "+name+";")