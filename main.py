from helpers import *
from costFunctions import *
from queries import *

GenerateExample('Uncle')

##Figure out why Bp [1,3] is reporting ('TP', 4, 'FN', 1, 'FP', 3, 'TN', 1)
#The TN=1 is it hitting (Noah,  but should that even be possible 

Ep=getListOfTables(POSITIVE_EXAMPLE_TYPE)[0]
Em=getListOfTables(NEGATIVE_EXAMPLE_TYPE)[0]
B=getListOfTables(BACKGROUND_TYPE)

tempTable=Table("temp",["t1c1"])
U=Table("U",["temp"])
copyToNewTable(Ep, U)
H=[] #List of Literals since they contain the table name and columnMapping

#TODO: All queries should run async and at the same time.
while U.size()>0:
	Tp=Table("Tp",["temp"])
	Tm=Table("Tm",["temp"])
	print(Ep.columns)
	copyToNewTable(U, Tp)
	copyToNewTable(Em, Tm)
	print(Tp.toString())
	Tp=Literal(Tp.name,defaultColumns(Tp.name,2),range(1,Tp.size()))
	Tm=Literal(Tm.name,defaultColumns(Tm.name,2),range(1,Tm.size()))
	
	notAllColumnsTouched=True
	currentClause=[]
	
	#TODO: Should be cache'd from calculations
	#TODO: Test that this stopping condition works
	#TODO: Check an example where the inner loop actually requires two steps
	
	while (Tm.size()!=0):# or (notAllColumnsTouched):
		candidateLiterals=generateCandidateLiterals(B,len(Tp.columns),H)
		print("Candidate Literal Length:")
		print(len(candidateLiterals))
		highestScore=-1
		highestCandidates=[]
		
		for candidate in candidateLiterals:
			score=CalculateAndSetScore(candidate,Tp,Tm)
			
			if score>highestScore:
				highestCandidates=[]
				highestScore=score
			if score==highestScore:
				highestCandidates.append(candidate)
		
		highestCandidate=chooseFromBestCandidates(highestCandidates,len(Tp.columns))
		
		print("Best Candidate:")
		print(highestCandidate.name)
		print(highestCandidate.columnMapping)
		currentClause.append(highestCandidate)
		
		#TODO: Super inefficient to do this seperately from the candidate scoring, 
		#but is proportionally small compared to the candidate scoring loop
		
		print("Are all columns touched?",areAllColumnsTouched(Ep,currentClause))
		notAllColumnsTouched=not areAllColumnsTouched(Ep,currentClause)
		print("-----------------------")
		print("Total Positive Examples: ",Tp.size())
		print("Total Negative Examples: ",Tm.size())
		
		
		copyResultsOfJoin(Tp, highestCandidate)
		print("tempTable")
		
		print(Tp.toString())
		print(Tm.toString())
		print(highestCandidate.toString())
		copyResultsOfJoin(Tm, highestCandidate) #Needs to be updated to only count target tuples that have columns included in the clause
		print(Tm.toString())
		print("Remaining Negative Examples: ",Tm.size())
		print("Remaining Positive Examples: ",Tp.size())
		print("-----------------------")
		
	for candidate in currentClause:
		H.append(candidate)
	
	t=Literal("tempU",U.columns,range(1,len(U.columns)))
	copyResultsOfAntiJoin(U,Tp,t)
	copyToNewTable(t,U)
	print(U.toString())
	
	print("Result:")
	for c in H:
		print(c.name,c.columnMapping)



