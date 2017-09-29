'''
Created on Sep 25, 2017

@author: rclaus
'''

import quickstep as q
from objects import *

q.ip='robertclaus.ddns.net'
q.format='table'

def buildWhere(table,literalCandidate):
    
    
    tableColumnCount=len(table.columns) #["c1","c2"]->2
    
    wheres=[]
    
    for idx,mapping in enumerate(literalCandidate.columnMapping):
        if(mapping<tableColumnCount+1):
            newWhere=table.columns[mapping-1]+"="+literalCandidate.name+"c"+str(idx+1)+" AND "
            wheres.append(newWhere)
    
    if(len(wheres)==0):
        return ""
    
    query=" WHERE "
    for where in wheres:
        query=query+where
    query=query[:-4]
    return query

def buildSingleSelect(table):
    query="SELECT "
    for col in table.columns:
        query=query+col+","
    query=query[:-1]+" "
    return query

def groupByTable(table):
    query="GROUP BY "
    for col in table.columns:
        query=query+col+","
    query=query[:-1]+" "
    return query

def buildCombinedSelect(table,literalCandidate):
    query="SELECT "
    for col in table.columns:
        query=query+col+","
    
    Zcol=""
    for ind,mapping in enumerate(literalCandidate.columnMapping):
        if mapping>len(table.columns):
            Zcol=literalCandidate.name+"c"+str(ind+1)+" AS "+table.name+"c"+str(len(table.columns)+1)+","
    
    query=query+Zcol
    query=query[:-1]+" "
    return query

def buildCombinedGroup(table,literalCandidate):
    query="GROUP BY "
    for col in table.columns:
        query=query+col+","
    
    Zcol=""
    for ind,mapping in enumerate(literalCandidate.columnMapping):
        if mapping>len(table.columns):
            Zcol=table.name+"c"+str(len(table.columns)+1)+","
    
    query=query+Zcol
    query=query[:-1]+" "
    return query

def defaultJoinColumns(table1,table2):
    columns=table1.columns[:]
    
    Zcol=""
    for ind,mapping in enumerate(table2.columnMapping):
        if mapping>len(table1.columns):
            Zcol=table1.name+"c"+str(len(table1.columns)+1)
    if Zcol!="":
        columns.append(Zcol)
    return columns


#TODO: Needs to be optimized to do the aggregation within the database
def countOfLeftJoin(table,literalCandidate):
    #Assumes table1 defines its tuples as (1,2)
    query=buildSingleSelect(table)+"FROM "+table.name+","+literalCandidate.name+buildWhere(table,literalCandidate)
    
    #This group by takes the result down as in section 3, but it's unclear whether it's the right move.
    #For D calculations this is appropriate.
    query=query+" "+groupByTable(table)+";"
    return q.sql_to_table(query).shape[0]
    
    #Same but without the group by.
    #TODO: Needs to be optimized to do aggregation in the database
def countOfJoin(table,literalCandidate):
        #Assumes table1 defines its tuples as (1,2)
    query=buildSingleSelect(table)+"FROM "+table.name+","+literalCandidate.name +buildWhere(table,literalCandidate)
    return q.sql_to_table(query).shape[0]


def countOf(tableOrLiteral):
    query="SELECT COUNT(*) AS c FROM "+tableOrLiteral.name+";"
    return int(q.sql_to_table(query).iloc[0]['c'])



def dropAndCreateTable(table):
    q.sql_to_text("DROP TABLE "+table.name+";")
    query="CREATE TABLE "+table.name+" ("
    for column in table.columns:
        query =query+column+" varchar(20),"
    query=query[:-1] # strip off last ','
    query = query+');'
    print(query)
    print(q.sql_to_text(query))
    return
    
    
def copyToNewTable(table,newTable):
    newTable.columns=[]
    for col in table.columns:
        newTable.columns.append(newTable.name+col[-2:])
    dropAndCreateTable(newTable)
    query="INSERT INTO "+newTable.name+" SELECT * FROM "+table.name
    q.sql_to_text(query)
    newTable.columns=table.columns
    return

def copyResultsOfJoin(table,literalCandidate):
    newCols=defaultJoinColumns(table,literalCandidate)
    newTable=Literal("temp"+table.name,newCols,range(1,len(newCols)))
    dropAndCreateTable(newTable)
    
    #Assumes table1 defines its tuples as (1,2)
    insert="INSERT INTO "+newTable.name+" "
    select=buildCombinedSelect(table, literalCandidate)+"FROM "+table.name+","+literalCandidate.name+buildWhere(table,literalCandidate)+buildCombinedGroup(table,literalCandidate)
    
    #This group by takes the result down as in section 3, but it's unclear whether it's the right move.
    #For D calculations this is appropriate.
    query=insert+select+";"
    print q.sql_to_text(query)
    print query
    copyToNewTable(newTable,table)
    return

def copyResultsOfAntiJoin(table,literalCandidate,newTable):
    dropAndCreateTable(newTable)
    
    #Bp antijoin Bb
    #SELECT * FROM Bp WHERE NOT EXISTS(SELECT Bbc2 FROM Bb WHERE Bpc2=Bbc2);
    
    insert="INSERT INTO "+newTable.name+" "
    outerSelect=buildSingleSelect(table)+"FROM "+table.name+"WHERE NOT EXISTS("
    innerSelect=buildSingleSelect(literalCandidate) +"FROM "+literalCandidate.name+buildWhere(table,literalCandidate)

    query=insert+outerSelect+innerSelect+");"
    q.sql_to_text(query)
    return
    
    