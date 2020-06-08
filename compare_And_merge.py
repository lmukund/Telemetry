#%%
import pandas as pd
import numpy as np
import csv

#%%
def readData(file1,file2):
    data1=pd.read_csv(file1)
    data2=pd.read_csv(file2)    
    data1=data1.iloc[:,:].values
    data2=data2.iloc[:,:].values
    return data1,data2

#%%
def makePools(data1,data2):
    li1=data1[:,0]
    li2=data2[:,0]
    li=np.concatenate((li1,li2))
    li=list(dict.fromkeys(li))
    return li1,li2,li

#%%
def makeTable(data): 
    table={}
    for row in data:
        key=row[0]
        valueList=row[1]
        if type(valueList)==float:
            table[key]=[]
            continue
        li=valueList.split(",")
        table[key]=li
    return table

#%%
def rawList(valuelist):
    tmpli=[]
    for string in valuelist:
        tmpli.append(string.split("==>")[0])
    return tmpli

#%%
def getVersion(item,valuelist):
    ans=""
    for field in valuelist:
        tmp=field.split("==>")
        if len(tmp)==1:
            continue
        if tmp[0]==item:
            ans=tmp[1]
            break
    return ans
    
#%%
def merge(table1,table2,li,li1,li2):
    table={}
    dict_table={}
    for key in li:
        res=[]
        if key in li1 and key in li2:
            valuelist1=table1[key]
            valuelist2=table2[key]
            rawlist1=rawList(valuelist1)
            rawlist2=rawList(valuelist2)
            rawlist=np.concatenate((rawlist1,rawlist2))
            rawlist=list(dict.fromkeys(rawlist))
            for item in rawlist:
                if item in rawlist1 and item in rawlist2:
                    v1=getVersion(item,valuelist1)
                    v2=getVersion(item,valuelist2)
                    v=v1+"&"+v2                    
                elif item in rawlist1:
                    v=getVersion(item,valuelist1)
                else:
                    v=getVersion(item,valuelist2)
                value=item+"==>"+v
                res.append(value)
            string=""
            for s in res:
                string=string+s+","
            string=string[:-1]
            table[key]=string
            dict_table[key]=res
        elif key in li1:
            string=""
            for s in table1[key]:
                string=string+s+","
            string=string[:-1]
            table[key]=string
            dict_table[key]=table1[key]
        else:
            string=""
            for s in table2[key]:
                string=string+s+","
            string=string[:-1]
            table[key]=string
            dict_table[key]=table2[key]
        
    return table,dict_table
   
#%%
def main(file1,file2):
    data1,data2 = readData(file1,file2)
    table1=makeTable(data1)
    table2=makeTable(data2)
    fieldlist1,fieldlist2,fieldlist=makePools(data1,data2)
    table,dict_table=merge(table1,table2,fieldlist,fieldlist1,fieldlist2)
    return table,dict_table
#%%
def writeToDatabase(wtable,name):
    with open(name, 'w') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(['field','value'])
        for key, value in wtable.items():
            writer.writerow([key, value])

#%%
a = input("Enter name for first file eg for data_1.csv: ")
b = input("Enter name for second file eg for data_2.csv: ")
#%%
file1=a
file2=b

#%%
table,dict_table=main(file1,file2)
c=input("wrting name : ")
writeToDatabase(table,c)  
    
#%%

    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    


        
    
    
    
    

