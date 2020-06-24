import pandas as pd
import numpy as np
import csv
#%%
def readFlaskDB():
    file = "flaskdb.csv"
    data=pd.read_csv(file)
    col_list=[]
    for col in data.columns:
        col_list.append(col)
    data=data.iloc[:,:].values
    return data

#%%
def check(block,value,data):
   for row in data:
       if type(row[1])==float:
           continue
       if block.lower() == row[0].lower() and value.lower() == row[1].lower():
           return True
   return False
#%%
def updateDescription(block,value,des,data):
    for row in data:
       if type(row[1])==float:
           continue
       if block.lower() == row[0].lower() and value.lower() == row[1].lower():
           row[3]=des
           break
    return data
#%%
def updateFlaskDB(data):
    with open("flaskdb.csv", 'w',newline='') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(['Information Block','Attribute','ISE Version','Description'])
        for item in data:
            writer.writerow(item)
#%%
def readBlackListDB():
    file="blacklist.csv"
    data=pd.read_csv(file)
    col_list=[]
    for col in data.columns:
        col_list.append(col)
    data=data.iloc[:,:].values
    return data    
#%%
            
def updateBlackListDB(data,value):
    towrite=[]
    for row in data:
        towrite.append(row[0])
    towrite.append(value)
    li=list(dict.fromkeys(towrite))
    with open("blacklist.csv", 'w',newline='') as csv_file:  
        writer = csv.writer(csv_file)
        writer.writerow(['Blacklisted'])
        for item in li:
            writer.writerow([item])
            
#%%
def getBlockValue(block,value,data):
    for row in data:
        if type(row[1])==float:
            continue
        if block.lower() == row[0].lower() and value.lower() == row[1].lower():
            return row[0],row[1]
    return "",""
#%%
def getBlackList(bdb):
    li=[]
    for item in bdb:
        li.append(item[0])
    return li
            
#%%
def hideInternalInfra(data):
    li=[]
    for row in data:
       if type(row[1])==float:
           continue
       if "_" in row[1]:
          li.append(row[1])
    return li
#%%
def updateNewDB(dbtype):
    if dbtype == 'flaskdb':
        newdata=pd.read_csv("validate.csv")
        data=newdata.iloc[:,:].values    
        with open("flaskdb.csv", 'w',newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Information Block','Attribute','ISE Version','Description'])
            for item in data:
                writer.writerow(item)
    else :
        newdata=pd.read_csv("validate.csv")
        data=newdata.iloc[:,:].values    
        with open("blacklist.csv", 'w',newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(['Blacklisted'])
            for item in data:
                writer.writerow(item)
    return



    
