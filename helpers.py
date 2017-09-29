'''
Created on Sep 22, 2017

@author: rclaus
'''


from objects import *
from queries import *
from sympy.logic.boolalg import false

TABLE_INDEX_NAME='TableIndex'
POSITIVE_EXAMPLE_TYPE='PositiveExample'
NEGATIVE_EXAMPLE_TYPE='NegativeExample'
BACKGROUND_TYPE='Background'
TEMPORARY_TABLE_NAME='temp'
CANDIDATE_PATTERNS = [[3,1],[3,2],[1,3],[1,2],[2,3],[2,1]]
TARGET_COLUMN_COUNT = 2
#0 is X, 1 is Y, 2 is Z from the paper





    
def getListOfTables(type):
    query="SELECT name FROM "+TABLE_INDEX_NAME+" WHERE type='"+type+"';"
    dataFrame= q.sql_to_table(query)
    tableList=[]
    for row in dataFrame.iterrows():
        name=row[1]['name']
        tempLiteral=Literal(name,defaultColumns(name,TARGET_COLUMN_COUNT),[1,2])
        tableList.append(tempLiteral)
    return tableList
    
    
def generateCandidateLiterals(B,currentColumnCount,alreadyUsedLiterals):
    possiblities=[]
    for table in B:
        for pattern in generateCandidatePatterns(currentColumnCount):
            patOk=True
            for lit in alreadyUsedLiterals:
                ok=False
                for litPatternIndex in range(0,len(lit.columnMapping)):
                    if lit.columnMapping[litPatternIndex]!=pattern[litPatternIndex]:
                        ok=True
                if ok==False:
                    patOk=False
            if patOk:
                possiblities.append(Literal(table.name,defaultColumns(table.name,TARGET_COLUMN_COUNT),pattern))
    return possiblities

def defaultColumns(name,count):
    temp=[]
    for c in range(1,count+1):
        temp.append(str(name)+"c"+str(c))
    return temp

#Taken from the wikipedia article on Heap's algorithm  (Non recursive version)
def generateCandidatePatterns(columnsInTestSet):
    possibleAssignments=list(range(1,columnsInTestSet+2))
    
    patterns=[]
    for x in possibleAssignments:
        for y in possibleAssignments:
            patterns.append([x,y])
    
    return patterns

def chooseFromBestCandidates(highestCandidates,currentColumnCount):

    for can in highestCandidates:
        #Remove candidates with duplicates
        firstIndex=can.columnMapping[0]
        for i in can.columnMapping[1:]:
            if firstIndex==i:
                can.score=can.score-2
            if i==currentColumnCount+1:
                can.score=can.score-1
    
    highScore=-100
    for can in highestCandidates:
        if can.score>highScore:
            highCan=can
            highScore=can.score
    
                
    return highCan
            

def areAllColumnsTouched(inLiteral,usingLiterals):
    
    for x in inLiteral.columnMapping:
        ok=False
        for usingLiteral in usingLiterals:
            for y in usingLiteral.columnMapping:
                if x==y:
                    ok=True
                    break
        if ok==False:
            return False
    return True
    



def populateFirstOrderTable(tableName,values,type):
    dropAndCreateTable(Literal(tableName,defaultColumns(tableName,2),[]))
    query="INSERT INTO "+tableName+" VALUES "
    for value in values:
        query="INSERT INTO "+tableName+" VALUES "
        query=query+"('"+value[0]+"', '"+value[1]+"'),"
        query=query[:-1] #Strip off last ','
        query=query+";"
        q.sql_to_text(query)
    
    q.sql_to_text("INSERT INTO "+TABLE_INDEX_NAME+" VALUES ('"+tableName+"','"+type+"');")

def GenerateExample(specificExample):
    if specificExample=='Uncle':
        #Setup Table Index
        #Drop/Create Tables
        #Populate Tables
        dropAndCreateTable(Literal(TABLE_INDEX_NAME,['name','type'],[]))
        
        Ep=[['Daniel','Jacob'],['Jason','Andrew'],['Noah','Andrew'],['Daniel','William']]
        Em=[['John','Jason'],['Noah','John'],['Jason','Justin'],['Noah','Justin']]
        Bb=[['Andrew','Jacob'],['Jason','Noah'],['Jacob','Andrew'],['Noah','Jason'],['Owen','William']]
        Bp=[['Daniel','Andrew'],['Jason','Jacob'],['Noah','Jacob'],['Noah','Justin'],['Jimmy','Jason'],['Daniel','Owen']]
        Bs=[['Daniel','June'],['Daniel','Jennifer'],['Daniel','Rachel'],['Daniel','Jason'],['John','William'],['Noah','Gwen'],['Jason','Sara']]

        populateFirstOrderTable('Ep', Ep, POSITIVE_EXAMPLE_TYPE)
        populateFirstOrderTable('Em', Em, NEGATIVE_EXAMPLE_TYPE)
        populateFirstOrderTable('Bb', Bb, BACKGROUND_TYPE)
        populateFirstOrderTable('Bp', Bp, BACKGROUND_TYPE)
        populateFirstOrderTable('Bs', Bs, BACKGROUND_TYPE)










































        
        
        