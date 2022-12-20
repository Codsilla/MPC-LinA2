
"""! @brief Python3.0 code to generate an LP cplex file with PWL costs for an instance of the cMCND. """

##
# @mainpage Python PWL LP file generation Project
#
# Example of function call: python3 MCNDbuildmodelgenerateLPfile.py test 03 6
#
#
#
# @section description_main Description
# An example Python program demonstrating how to generate a PWL LP file
# for a given instance and pwl function
#
# @section notes_main Notes
# - subfunctions 'readformateddatafiles' and 'readpwldatafiles' are supposed
# to read data files. However, the output of 'readformateddatafiles' is to be completed
# - subfunction 'MCNDbuildmodelgenerateLPfile' create the PWL LP model and
# writes it in an LP file
#
# Copyright (c) 2022 S.U.N.  All rights reserved.


import sys
import cplex
import csv
#from math import *
#import random
import numpy as np
#import pickle
#import sys
#import datetime
#import matplotlib.pyplot as plt
#from matplotlib import patches
#import time
#import socket

def getcardN(allArcs):
    cardN=-1
    print("todebug")
    print(allArcs)
    for lines in allArcs:
        print("todebug")
        print(lines)
        cardN=int(max(cardN,int(lines["from"]),int(lines["to"])))
    
    print(cardN)
    return cardN
    
    
def getArcsInfo(cardN,allArcs):
    dictArcs = {};
    
    arcExistsIJ = [[0 for j in range(cardN)] for i in range(cardN)]
    OfixedCostIJ = [[0.0 for j in range(cardN)] for i in range(cardN)]
    DvarcostIJ = [[0.0 for j in range(cardN)] for i in range(cardN)]
    UcapIJ = [[0.0 for j in range(cardN)] for i in range(cardN)]
        
    for lines in allArcs:
        print("todebug2222")
        print(lines)
        orig=int(lines["from"])-1 #-1 because nodes start at 1 in data file, but at 0 in python code
        dest=int(lines["to"])-1 #-1 because nodes start at 1 in data file, but at 0 in python code
        
        arcExistsIJ[orig][dest]=1
        OfixedCostIJ[orig][dest]=float(lines["fixed_cost"])
        DvarcostIJ[orig][dest]=float(lines["variable_cost"])
        UcapIJ[orig][dest]=float(lines["capacity"])
    
    dictArcs["arcExistsIJ"]=arcExistsIJ
    dictArcs["OfixedCostIJ"]=OfixedCostIJ
    dictArcs["DvarcostIJ"]=DvarcostIJ
    dictArcs["UcapIJ"]=UcapIJ
    
    return dictArcs
    
    
def getcardP(allCommod):
    cardP=0
    for lines in allCommod:
        cardP=cardP+1
    
    print(cardP)
    return cardP


def getCommodInfo(cardP,allCommod):
    dictCommod={}
    
    OriginP = [0 for i in range(cardP)]
    DestP = [0 for i in range(cardP)]
    DemandP = [0 for i in range(cardP)]
    
    p=0
    for lines in allCommod:
        print("todebug3333")
        print(lines)
        
        OriginP[p]=int(lines["from"])-1 #-1 because nodes start at 1 in data file, but at 0 in python code
        DestP[p]=int(lines["to"])-1 #-1 because nodes start at 1 in data file, but at 0 in python code
        DemandP[p]=int(lines["quantity"])
        
        p=p+1

    dictCommod["OriginP"]=OriginP
    dictCommod["DestP"]=DestP
    dictCommod["DemandP"]=DemandP

    return dictCommod
    

def getNodesInfo(cardN,allNodes):
    dictNodes={}
    
    initCapaI = [0.0 for i in range(cardN)]
    incrCapaI = [0.0 for i in range(cardN)]
    
    for lines in allNodes:
        print("todebug4444")
        print(lines)
        node=int(float(lines["node"]))-1 #-1 because nodes start at 1 in data file, but at 0 in python code
        
        initCapaI[node]=float(lines["InitCapacity"])
        incrCapaI[node]=float(lines["IncremCapacity"])
    
    dictNodes["InitCapacity"]=initCapaI
    dictNodes["IncremCapacity"]=incrCapaI
    
    return dictNodes


def readformateddatafiles(instance, ref):
    """! reads the 3 cMCND data files
    @param instance   The name of the instance.
    @param ref   03 or 08.
    @return  /. ???? ---> TODO: output data to feed the model !!!!!!!!!
    """
    
    allArcs = []
    allNodes= []
    allCommod=[]
    
    # opening the CSV file
    with open("formatedData/"+instance+".csv", mode ='r') as file:
        # reading the CSV file
        csvArcs = csv.DictReader(file)
        # displaying the contents of the CSV file
        for lines in csvArcs:
            allArcs.append(dict(lines))
            print(lines)
            print(lines["from"])
            


    with open("formatedData/"+instance+"Commod.csv", mode ='r') as file:
        # reading the CSV file
        csvCommod = csv.DictReader(file)
        # displaying the contents of the CSV file
        for lines in csvCommod:
            allCommod.append(dict(lines))
            print(lines)
            print(lines["from"])

    with open("formatedData/infoNodes/nodes_"+instance+"_"+ref+".csv", mode ='r') as file:
        # reading the CSV file
        csvNodes = csv.DictReader(file)
        # displaying the contents of the CSV file
        for lines in csvNodes:
            allNodes.append(dict(lines))
            print(lines)
            print(lines["node"])
            print(type(lines["node"][0]))

    cardN=getcardN(allArcs)
    Arcs = getArcsInfo(cardN,allArcs)
    
    cardP=getcardP(allCommod)
    Commod = getCommodInfo(cardP,allCommod)
    
    Nodes = getNodesInfo(cardN,allNodes)
    
    return cardN, Arcs, cardP, Commod, Nodes
    
            
def readpwldatafiles(instance, variant03or08, incremcost6or7or8, pwlorigin):
    """! reads the 2 PWL data files
    @param instance  The name of the instance whose PWL data files
                        should be read. Those files will have an extension '.bpx'
                        or '.bpval'
    @return  bpx, bpval (the x and y coordinates of the breakpoints, 0,0 included !)
    """
    
    bpx=[]
    bpval=[]
    # opening the CSV file
    with open("pwlData/"+pwlorigin+"/"+instance+"_"+variant03or08+"_"+incremcost6or7or8+".bpx", mode ='r') as file:
        # reading the CSV file
        csvFile = csv.DictReader(file)
        # displaying the contents of the CSV file
        for lines in csvFile:
            #print(lines)
            #print(lines[None])
            try:
                new_list = [float(element) for element in lines[None]]
                bpx.append(new_list)
                #print("The list of floats is:")
                #print(new_list)
            except ValueError:
                print("Some values in the input list can't be converted to float.")
    
    print("\nbpx=")
    print(bpx)
    
    with open("pwlData/"+pwlorigin+"/"+instance+"_"+variant03or08+"_"+incremcost6or7or8+".bpval", mode ='r') as file:
        # reading the CSV file
        csvFile = csv.DictReader(file)
        # displaying the contents of the CSV file
        for lines in csvFile:
            #print(lines)
            #print(lines[None])
            try:
                new_list = [float(element) for element in lines[None]]
                bpval.append(new_list)
                #print("The list of floats is:")
                #print(new_list)
            except ValueError:
                print("Some values in the input list can't be converted to float.")
    
    print("\nbpval=")
    print(bpval)
    return bpx, bpval






def writePWLmodelinLPfile(model,outputlpfilename):
    """! generates a PWL LP file
    @param model   The model to write.
    @param outputlpfilename   The name of the written file.
    @return  /.
    """

    print(" Write lp file "+outputlpfilename+"\n")
    
    model.write(outputlpfilename)




def MCNDbuildPWLmodel(cardN,arcExistsIJ,OfixedCostIJ,DvarcostIJ,UcapIJ,cardP,OriginP,DestP,DemandP,initCapaI,incrCapaI,Bpx,Bpcost):
    """! Builds the cplex model from all loaded data
    @return  The model.
    """
    
    print("\n Initialisation Cplex model\n")
    model=cplex.Cplex() #creation du probleme cplex
    #test_temps=model.get_time() #date creation cplex
    model.objective.set_sense(1) #on indique qu'on va minimiser la fonction
    
    Xijp = [[[0 for p in range(cardP)] for j in range(cardN)] for i in range(cardN)] #stocke la variable Xijk
    Yij = [[0 for j in range(cardN)] for i in range(cardN)] #stocke la variable Yijl
    Vi = [0 for j in range(cardN)] #stocke la variable Vi
    
    # sumDkXijk = [[0 for j in range(cardN)] for i in range(cardN)] #stocke la variable sumDkXijk
    CostFi = [0 for i in range(cardN)] #stocke la variable CostFi

    print(" cardN="+str(cardN)+",  cardIJ="+str(np.sum(arcExistsIJ))+", cardP="+str(cardP)+"\n")

    #definition variables Xijp
    for i in range(cardN):
        for j in range(cardN):
            if arcExistsIJ[i][j] > 0:
                for p in range(cardP):
                    Xijp[i][j][p]="Xijp("+str(i)+","+str(j)+","+str(p)+")"
                    model.variables.add(obj = [DvarcostIJ[i][j]],
                        types = [model.variables.type.continuous],
                        names = [Xijp[i][j][p]])

    #definition variables Yij
    for i in range(cardN):
        for j in range(cardN):
            if arcExistsIJ[i][j] > 0:
                Yij[i][j]="Yij("+str(i)+","+str(j)+")"
                model.variables.add(obj = [OfixedCostIJ[i][j]],
                    types = [model.variables.type.binary],
                    names = [Yij[i][j]])

    #definition variables Vi
    for i in range(cardN):
        Vi[i]="Vi("+str(i)+")"
        model.variables.add(#obj = [0.0],
                types = [model.variables.type.continuous],
                names = [Vi[i]],
                ub=[initCapaI[i]+incrCapaI[i]])

    #definition variables CostFi
    for i in range(cardN):
        CostFi[i]="CostFi("+str(i)+")"
        model.variables.add(obj = [1.0],
                                types = [model.variables.type.continuous],
                                names = [CostFi[i]])

    #definition constraint flowbalance
    for p in range(cardP):
        origP = OriginP[p];
        destiP = DestP[p];
        for i in range(cardN):
            theind = []
            theval= []
            if origP == i:
                therhs = DemandP[p]
            elif destiP == i:
                therhs = -DemandP[p]
            else:
                therhs = 0.0
            for j in range(cardN):
                if arcExistsIJ[i][j] > 0:
                    theind.append(Xijp[i][j][p])
                    theval.append(1.0)
                if arcExistsIJ[j][i] > 0:
                    theind.append(Xijp[j][i][p])
                    theval.append(-1.0)
            model.linear_constraints.add(lin_expr=[[theind,theval]], senses=["E"], rhs=[therhs], names =["flowbalance("+str(i)+","+str(p)+")"])

    #definition constraint noarcnoflow
    for i in range(cardN):
        for j in range(cardN):
            if arcExistsIJ[i][j] > 0:
                for p in range(cardP):
                    theind = []
                    theval= []
                    theind.append(Yij[i][j])
                    theval.append(-DemandP[p])
                    theind.append(Xijp[i][j][p])
                    theval.append(1.0)
                    model.linear_constraints.add(lin_expr=[[theind,theval]], senses=["L"], rhs=[0.0], names =["noarcnoflow("+str(i)+","+str(j)+","+str(p)+")"])
                    
    #definition constraint arccapacity
    for i in range(cardN):
        for j in range(cardN):
            if arcExistsIJ[i][j] > 0:
                theind = []
                theval= []
                theind.append(Yij[i][j])
                theval.append(-UcapIJ[i][j])
                for p in range(cardP):
                    theind.append(Xijp[i][j][p])
                    theval.append(1.0)
                model.linear_constraints.add(lin_expr=[[theind,theval]], senses=["L"], rhs=[0.0], names =["arccapacity("+str(i)+","+str(j)+")"])

    #definition constraint computevi
    for i in range(cardN):
        theind = []
        theval= []
        theind.append(Vi[i])
        theval.append(-1.0)
        for j in range(cardN):
            if arcExistsIJ[j][i] > 0:
                for p in range(cardP):
                    theind.append(Xijp[j][i][p])
                    theval.append(1.0)
        model.linear_constraints.add(lin_expr=[[theind,theval]], senses=["E"], rhs=[0.0], names =["computevi("+str(i)+")"])

    #contrainte fonction lineaire par morceau
    for i in range(cardN):
        model.pwl_constraints.add(vary=CostFi[i],
                          varx=Vi[i],
                          preslope= 0,
                          postslope= 0,
                          breakx=Bpx[i],
                          breaky=Bpcost[i],
                          name='pwl'+str(i))
                          
    return model


#Example of function call: python3 MCNDbuildmodelgenerateLPfile.py test 03 6

assert(len(sys.argv) > 4), "ERROR !!!! insufficient number of input arguments !!!! should be : instancename, variant03or08, incremcost6or7or8, pwlorigin\n"

instancename=sys.argv[1]
variant03or08=sys.argv[2]
incremcost6or7or8=sys.argv[3]
pwlorigin=sys.argv[4]

assert((variant03or08 == "03") or (variant03or08 == "08")), "ERROR on input 'variant03or08' !!! should be '03' or '08'"

assert((incremcost6or7or8 == "6") or (incremcost6or7or8 == "7") or (incremcost6or7or8 == "8") ), "ERROR on input 'incremcost6or7or8' !!! should be '6' or '7' or '8'"

assert((pwlorigin == "Lina") or (pwlorigin == "naive") ), "ERROR on input 'pwlorigin' !!! should be 'Lina' or 'naive'"


#cardN, Arcs, cardP, Commod, Nodes = readformateddatafiles("test", "03")
cardN, Arcs, cardP, Commod, Nodes = readformateddatafiles(instancename, variant03or08)

bpx, bpval = readpwldatafiles(instancename, variant03or08, incremcost6or7or8, pwlorigin)

model = MCNDbuildPWLmodel(cardN,  Arcs["arcExistsIJ"] ,  Arcs["OfixedCostIJ"] ,  Arcs["DvarcostIJ"] ,  Arcs["UcapIJ"] , cardP , Commod["OriginP"] , Commod["DestP"] , Commod["DemandP"] , Nodes["InitCapacity"], Nodes["IncremCapacity"], bpx, bpval)

writePWLmodelinLPfile(model,"output/"+instancename+"_"+variant03or08+"_"+incremcost6or7or8+"_pwl_"+pwlorigin+".lp")

print("done")
