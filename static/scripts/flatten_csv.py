import pandas as pd
import numpy as np
import copy as cp
import re
import csv
#from json2table import convert
#%%
def readFile(file):
    data1=pd.read_csv(file)
    return data1

#%%
def getColumnName(data):
    col_list=[]
    for col in data.columns: 
        col_list.append(col)
    colName=np.array(col_list).reshape(1,len(col_list))    
    return colName
#%%
def dataFrameToArray(data):
    dataArray=data.iloc[:,:].values
    return dataArray

#%%
def filteredLeafData(leaf_data):    
    new_leaf=[]    
    for i in range(leaf_data.shape[1]):
        head=leaf_data[0,i]
        head=head.split(".")
        if "type" in head or "name" in head or "type{}" in head or "items{}" in head or "items" in head:
            new_leaf.append(leaf_data[:,i])
        else:
            continue
    new_leaf=np.array(new_leaf).transpose()
    return new_leaf

#%%
def split(delimiters, string, maxsplit=0):
    regexPattern = '|'.join(map(re.escape, delimiters))
    res=re.split(regexPattern, string, maxsplit)
    res=' '.join(res).split()
    return res
#%%    
def categoryList(newLeafData):        
    category=newLeafData[0,:]
    category_list=[]
    delimiters=".","{}"
    for i in category:
        i=split(delimiters,i,0)
        category_list.append(i)
    return category_list

#%%
def isAllowed(li):
    if li[-1]=='type':
        return 0
    return 1

#%%
def makeTable(new_leaf,category_list,version):
    table={} 
    dict_table={}
    for i in range(1,new_leaf.shape[0]):
        row = new_leaf[i,:]
        key = row[0]
        li = []
        for j in range(1,len(row)):
            if isAllowed(category_list[j])==0:
                continue
            tmp = row[j]
            if type(tmp)==float:
                continue
            if tmp==key:
                continue
            tmp = tmp.split()
            tmp = list(dict.fromkeys(tmp))
            for field in tmp:
                li.append(field)
        li=list(dict.fromkeys(li))
        for j in range(len(li)):
            li[j]=str(li[j])+"==>"+str(version)
        string=""
        for s in li:
            string=string+s+","
        string=string[:-1]
        table[key] = string
        dict_table[key]=li
    return table,dict_table
    
#%%
def main(file,version):
    data=readFile(file)
    colName=getColumnName(data)
    data=dataFrameToArray(data)
    newData=np.vstack((colName,data))
    parentNode=cp.deepcopy(newData[:,0])
    leafData=cp.deepcopy(newData[:,:])
    newLeafData=filteredLeafData(leafData)
    category_list=categoryList(newLeafData)
    table,dict_table=makeTable(newLeafData,category_list,version)
    return table,dict_table
#%%
version=input("Enter Version of telemetry avro file (use capital o 'O' in place of zero(0)): \n")
file=input("enter file name with path (for eg 'data.csv'):  \n")
table,dict_table=main(file,version)
writing_name=input("enter name of output file (eg 'op_data.csv'): \n")
with open(writing_name, 'w') as csv_file:  
    writer = csv.writer(csv_file)
    writer.writerow(['field','value'])
    for key, value in table.items():
        writer.writerow([key, value])
#%%
  

        
        
    