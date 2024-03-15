import numpy as np
import copy
from decimal import Decimal
from itertools import product
from timeit import default_timer as timer

# ---- Module for generating Schur and LLT polynomials ---- #

# Classes:
# - Partition: A (possibly skew) partition lambda/mu
#       data: in outer partition `lam' and an inner partition `mu'
#       methods: `TabList(n)' generates all SSYT with fillings in {1,2,...,n}
#
# - Schur: A Schur polynomial of a given shape
#       data: a partition `shape'
#       methods: `__xWeight(tab,n)' gives the weight of the given semistandard filling tab in n variables
#                `poly(n)' returns the Schur polynomial of shape `shape' with n variables
#                `__tikzTab(tab,n,offset,color)' generates tikz code for drawing the tableaux tab as paths
#                `tikz(n)' generates tikz code for creating a table with all the SSYT of shape `shape' drawn as paths (and their weights)
#
# - LLT: An LLT polynomial of a given tuple of shapes
#       data: a tuple of partitions `partition_list'
#       methods: `__xWeight(tab,n)' gives the weight of the given semistandard filling tab in n variables
#                `__tWeight(tab0,tab1)' computes the number of coinversions between a pair of tableaux
#                `poly(n)' returns the LLT polynomial of indexed by the tuple of partitions `partition_list' with n variables
#                `__tikzTab(tab,n,offset,color)' generates tikz code for drawing the tableaux tab as paths
#                `tikz(n)' generates tikz code for creating a table with all the tuples of SSYT of shapes given by `partition_list' drawn as paths (and their weights)



# Notes:
# - For LLT stuff the partitions are assumed to be the same length. Must pad shorter partitions with zero parts.
# - In any function that takes in a tableaux, the tableaux are assumed to be padded with a zero at the start of each row and an inf at the end.
#       This helps when finding co-inversions. 
# - Because LLT polynomials with one part per partition are equal to Hall-Littlewood polynomials
#       we can also get Hall-Littlewood polynomails with at most two columns.

# Todo List:
#   Easy things:
# - wrappings (this would get all modified Macdonald polynomials)
# - check some timings
#
#   Harder things:
# - my refinemnt indexed by pairs of partitions and a matching
#
#   Other things:
# - list standard young tableaux
# - skyline fillings and related. Could compute keys, atoms, etc
# - could create a tableaux class with its own methods ie __tikzTab and __xWeight (would clean up some clutter).
#       It could also contain info like the content. This would make it easy to find generate all tableau with a given content ie Kosta numbers.
#       Could use this to compute schur expansions
# - could use sympy to simplify the expression of the polynomials and stuff like that
# - could have the tikz code create its own tex file so I wouldn't have to keep copy/pasting things
# - tikz code to draw tableaux fillings


inf = np.inf
colors=["blue","red","green","yellow"] # pick your own colors

class Tableau:
    def __init__(self, fill = []):
        self.filling = fill

    def getContent(self,nVar):
        content = [0] * nVar
        if self.filling != []:
            pass
            
        return content

    def xWeight(self):
        xpow = [0] * nVar
        return xpow

    def tikzTabPath(self):
        tikzstr = ""
        return tikzstr
    
    def tikzTabYD(self):
        tikzstr = ""
        return tikzstr

class Partition:
    def __init__(self, lam = [], mu = []):
        self.lam = lam
        self.mu = mu

    def TabList(self,nVar, Type="semistandard"):
        if Type == "semistandard":
            return self.TabListSS(nVar)

    def TabListSS(self,nVar):
        tablist0=[[]]
        tablist1=[]

        lam = self.lam
        if self.mu == []:
            mu = [[0]] * len(lam)
        else:
            mu = self.mu
        
        
        for row in range(len(lam)):
            for col in range(lam[row][0]+2):
                for tab in tablist0:
                    if col<=mu[row][0]:
                        tab0=copy.deepcopy(tab)
                        if col==0:
                            tab0.append([0])
                        else:
                            tab0[row].append(0)
                        tablist1.append(tab0)
                    elif col==lam[row][0]+1:
                        tab0=copy.deepcopy(tab)
                        tab0[row].append(inf)
                        tablist1.append(tab0)
                    else:
                        for n in range(1,nVar+1):
                            if row==0:
                                if n>=tab[row][col-1]:
                                    tab0=copy.deepcopy(tab)
                                    tab0[row].append(n)
                                    tablist1.append(tab0)
                            else:
                                if n>=tab[row][col-1] and n>tab[row-1][col]:
                                    tab0=copy.deepcopy(tab)
                                    tab0[row].append(n)
                                    tablist1.append(tab0)
                        
                tablist0=copy.deepcopy(tablist1)
                tablist1=[]

        return tablist0

class Schur:
    def __init__(self, partition=Partition()):
        self.shape = partition

    def __xWeight(self,tab,nVar):
        xpow = [0] * nVar
        for i in range(len(tab)):
            for j in range(1,len(tab[i])):
                if tab[i][j] != 0 and tab[i][j] != inf:
                    xpow[tab[i][j]-1]+=1
        return xpow

    def poly(self,nVar):
        polystr = ""
        tl=self.shape.TabList(nVar)

        first = True
        for tab in tl:
            if first:
                first=False
            else:
                polystr = polystr + " + "
            xpow = self.__xWeight(tab,nVar)
            for i in range(len(xpow)):
                if xpow[i]==1:
                    polystr = polystr + "x"+str(i+1)+" "
                elif xpow[i]>1:
                    polystr = polystr + "x"+str(i+1)+"^"+str(xpow[i])+" "

        return polystr

    def __tikzTab(self,tab,nVar,offset,color): # color is a str
        tikzstr=""
        k=0
        for row in tab:
            val = next((index for index,value in enumerate(row) if value != 0), None)
            startpos = Decimal(str(0.5+offset+val))-k
            tikzstr += r"\draw[ultra thick,"+color+"] ("+str(startpos)+",0)"
            for i in range(val,len(row)-1):
                tikzstr+= "--("+str(i-val+startpos)+","+str(row[i]-0.5+offset)+")--("+str(i-val+1+startpos)+","+str(row[i]-0.5+offset)+")"
            tikzstr+="--("+str(len(row)-val-1+startpos)+","+str(nVar)+");\n"
            k+=1
        

        return tikzstr

    def tikz(self,nVar):
        tl = self.shape.TabList(nVar)
        lam = self.shape.lam
        mu = self.shape.mu 
        
        tikzstr = r"\resizebox{\textwidth}{!}{"+"\n"
        tikzstr += r"\begin{tabular}{" + "c"*len(tl)+"}\n"
        weightstr = ""
        nColumns=lam[0][0]+len(lam)
        first = True
        for tab in tl:
            if first:
                first = False
            else:
                tikzstr += "&\n"
                weightstr += "& "
                
            tikzstr += r"\begin{tikzpicture}"+"\n"+r"\draw (0,0) grid ("+str(nColumns)+","+str(nVar)+");\n"
            tikzstr += self.__tikzTab(tab,nVar,0,"blue")
            tikzstr += r"\end{tikzpicture}"+"\n"
            weightstr += "$"
            xpow = self.__xWeight(tab,nVar)
            for i in range(len(xpow)):
                if xpow[i]==1:
                    weightstr += "x_{"+str(i+1)+"}"+" "
                elif xpow[i]>1:
                    weightstr += "x_{"+str(i+1)+"}^"+"{"+str(xpow[i])+"}"+" "
            weightstr += "$ "
        tikzstr += r"\\" + "\n"
        tikzstr += weightstr + "\n"
        tikzstr += r"\end{tabular}"+"\n}"
        
        return tikzstr


class LLT:
    def __init__(self,ptuple=[Partition()]):
        self.partition_list =  ptuple

    def __xWeight(self,tab,nVar):
        xpow = [0] * nVar
        for i in range(len(tab)):
            for j in range(1,len(tab[i])):
                if tab[i][j] != 0 and tab[i][j] != inf:
                    xpow[tab[i][j]-1]+=1
        return xpow

    def __tWeight(self,tab0,tab1):
        tpow = 0
        #print(tab0,tab1)
        for i in range(len(tab0)):
            for j in range(len(tab0[i])):
                if tab0[i][j] != 0 and tab0[i][j] != inf:
                    #print(i,j, tab0[i][j])
                    for k in range(len(tab1)):
                        l=k-i+j
                        if l>0 and l<len(tab1[k]):
                            #print("here: ",k,l,tab1[k][l],len(tab1[k]))
                            if tab1[k][l-1]<=tab0[i][j]<=tab1[k][l]:
                                tpow+=1
        #print("total tpow: "+str(tpow))
        return tpow

    def poly(self,nVar):
        polystr = ""

        TT=[pp.TabList(nVar) for pp in self.partition_list]
        tabtuplelist = list(product(*TT))

        first = True
        for tabtuple in tabtuplelist:
            xpow = [0]*nVar
            for tab in tabtuple:
                xpow = np.add(xpow,self.__xWeight(tab,nVar))
            tpow = 0
            if len(tabtuple)>1:
                for a in range(len(tabtuple)-1):
                    for b in range(a+1,len(tabtuple)):
                        tpow += self.__tWeight(tabtuple[a],tabtuple[b])
                
            if first:
                first=False
            else:
                polystr = polystr + " + "

            for i in range(nVar):
                if xpow[i]==1:
                    polystr = polystr + "x"+str(i+1)+" "
                elif xpow[i]>1:
                    polystr = polystr + "x"+str(i+1)+"^"+str(xpow[i])+" "

            if tpow==1:
                polystr = polystr + "t"+" "
            elif tpow>1:
                polystr = polystr + "t^"+ str(tpow)+" "

        return polystr
        


    def __tikzTab(self,tab,nVar,offset,color="black"): # color is a str
        tikzstr=""
        k=0
        for row in tab:
            val = next((index for index,value in enumerate(row) if value != 0), None)
            startpos = Decimal(str(0.5+offset+val))-k
            tikzstr += r"\draw[ultra thick,"+color+"] ("+str(startpos)+",0)"
            for i in range(val,len(row)-1):
                tikzstr+= "--("+str(i-val+startpos)+","+str(row[i]-0.5+offset)+")--("+str(i-val+1+startpos)+","+str(row[i]-0.5+offset)+")"
            tikzstr+="--("+str(len(row)-val-1+startpos)+","+str(nVar)+");\n"
            k+=1
        

        return tikzstr

    def tikz(self,nVar,ntable):
        TT=[pp.TabList(nVar) for pp in self.partition_list]
        tabtuplelist = list(product(*TT))

        nColumns = max(partition.lam[0][0] for partition in self.partition_list) + len(self.partition_list[0].lam)

        tikzstr = r"\resizebox{\textwidth}{!}{"+"\n"
        tikzstr += r"\begin{tabular}{" + "c"*ntable+"}\n"
        weightstr = ""

        counter = 0
        first = True
        for tabtuple in tabtuplelist:
            if first:
                first = False
                weightstr = ""
            else:
                tikzstr += "&\n"
                weightstr += "& "
                
            tikzstr += r"\begin{tikzpicture}"+"\n"+r"\draw (0,0) grid ("+str(nColumns)+","+str(nVar)+");\n"
            xpow = [0]*nVar
            nshift = -(len(self.partition_list)+1)//2
            ind = 0
            for tab in tabtuple:
                tikzstr += self.__tikzTab(tab,nVar,0.1*nshift,colors[ind])
                nshift += 2
                ind += 1
                xpow = np.add(xpow,self.__xWeight(tab,nVar))
            tikzstr += r"\end{tikzpicture}"+"\n"

            weightstr += "$"
            tpow = 0
            if len(tabtuple)>1:
                for a in range(len(tabtuple)-1):
                    for b in range(a+1,len(tabtuple)):
                        tpow += self.__tWeight(tabtuple[a],tabtuple[b])
            
            for i in range(len(xpow)):
                if xpow[i]==1:
                     weightstr += "x_{"+str(i+1)+"} "
                elif xpow[i]>1:
                    weightstr += "x_{"+str(i+1)+"}^"+"{"+str(xpow[i])+"}"+" "

            if tpow==1:
                weightstr += "t"
            elif tpow>1:
                weightstr += "t^{" + str(tpow) + "}"
            weightstr += "$"
            
            if counter == ntable-1:
                tikzstr += r"\\"+"\n"
                tikzstr += weightstr +"\n" + r"\\" + "\n"
                counter = 0
                first = True
            else:
                counter+=1
        else:
            if counter != 0:
                tikzstr += r"\\"+"\n"
                tikzstr += weightstr +"\n" + r"\\" + "\n"
            
        tikzstr += r"\end{tabular}"+"\n}"
        return tikzstr
                
    

    

lam1 = [[2],[2]]
lam2 = [[1],[0]]
##
p1=Partition(lam1, lam2)
# print(p1.TabList(2))
# p2=Partition(lam2)
##
# l=LLT([p1.TabList()])
# print(p1[0])

# lam1 = [[2],[0]]
# mu1 = [[1],[0]]
# lam2 = [[1],[1]]
# mu2 = [[1],[1]]
# ##
# p1=Partition(lam1)
# p2=Partition(lam2)
# p3=Partition(mu1)
# p4=Partition(lam2,mu1)
# l=LLT([p1,p2,p3,p4])
# print(l.tikz(3,10))
# ##
# l=LLT([p1,p2,p3,p4])
#print(Partition([[3],[2]],[[1],[1]]).TabList(3))
#print(l.poly(3))
#print(l.tikz(3,10))