'''
Created on Sep 22, 2017

@author: rclaus
'''

import math
from queries import *

def CalculateAndSetScore(candidate,positiveTestLiteral,negativeTestLiteral):
    beta=2
    
    Tp=int(countOf(positiveTestLiteral))
    Tm=int(countOf(negativeTestLiteral))
    Dp=int(countOfLeftJoin(positiveTestLiteral,candidate))
    Dm=int(countOfLeftJoin(negativeTestLiteral,candidate))
    Tpp=int(countOfJoin(positiveTestLiteral,candidate))
    Tmp=int(countOfJoin(negativeTestLiteral,candidate))
    
    print("Tp",Tp,"Tm",Tm,"Dp",Dp,"Dm",Dm,"Tpp",Tpp,"Tmp",Tmp)
    
    TP=Dp #D+ Needs to be updated to a left semi join instead of an equijoin
    FN=Tp-Dp# T+-D+
    FP=Dm#D- Needs to be updated to a left semi join instead of an equijoin
    TN=Tm-Dm # T--D-
    
    print("Candidate:")
    print(candidate.name,candidate.columnMapping)
    
    print("Values:")
    print("TP",TP,"FN",FN,"FP",FP,"TN",TN)
    
    mcc= MCC(TP,TN,FP,FN)
    
    auep=AUE(Tpp,Tmp)
    auepp=AUE(Tp,Tm)
    
    beta=2
    print(mcc,auep,auepp)
    score=SCORE(mcc,auep,auepp,beta)
    print("Score:",score)
    candidate.score=score
    return score

def MCC(TP,TN,FP,FN):
    d1=(TP+FP)
    d2=(TP+FN)
    d3=(TN+FP)
    d4=(TN+FN)
    if d1==0 or d2==0 or d3==0 or d4==0:
        return 0
    return ((TP*TN) - (FP*FN)) / math.sqrt(d1*d2*d3*d4)

def AUE(Tp,Tm):
    if Tp+Tm==0:
        return 0
    
    p=Tp/(Tp+Tm)
    
    if(p==0 or p==1):
        return 0
    part1=(p-1)*(p-1)*math.log(1-p,2)
    part2=p*p*math.log(1-p,2)
    part3=p/math.log(2)
    return .5*(part1-part2+part3)*(2*math.log(2))

def SCORE(mcc,auep,auepp,beta):
    numerator=1+(beta*beta)
    if mcc==-1:
        return 0
    denomenator1=beta*beta*(1/(mcc+1))
    denomenator2=1/(auepp-auep+1)
    print(numerator,denomenator1,denomenator2)
    return numerator/(denomenator1+denomenator2)

