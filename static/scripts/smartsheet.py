import pandas as pd
import numpy as np
import csv
name=input("enter file name eg : data.csv : \n")

data=pd.read_csv(name)
col_list=[]
#%%
for col in data.columns:
    col_list.append(col)
colName=np.array(col_list).reshape(1,len(col_list))
data=data.iloc[:,:].values

#%%
import copy
data1=copy.deepcopy(data)
#%%
for row in data:
    if type(row[1])==float:
        continue
    row[1]=row[1].split(",")
#%%
newd=[]
for row in data:
    block=row[0]
    attribue_list=row[1]
    if type(attribue_list)==float:
        newd.append([block,"","",""])
        continue
    for item in attribue_list:
        li=item.split("==>")
        attribute=li[0]
        if attribute=='null':
            continue
        version=li[-1]
        des=""
        newd.append([block,attribute,version,des])
    
#%%    
        
writing_name=input("enter name of output file (eg 'op_data.csv'): \n")
with open(writing_name, 'w',newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(['Information Block','Attribute','ISE Version','Description'])
    for item in newd:
        writer.writerow(item)
#%%
print("!!DONE!!")
#%%