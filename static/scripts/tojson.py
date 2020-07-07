import json
import copy
file=input("Enter avro file name with path (with extension like 'file.avsc') : ")
f=open(file)
j=json.load(f)
log=j['fields']

#%%
count=0
for row in log:
    if row['name']=="message_dispatched" or row['name']=="payload":
        count+=1
    for row in log:
        if row['name']=="payload":
            data=copy.deepcopy(row);
            break;
if count==2:
    for row in log:
        if row['name']=="payload":
            data=copy.deepcopy(row);
            break;        
    data=data['type']
    data=data['fields']  
    for row in data:
        if row['name']=='payload':
            data=row
            break
    data=data['type']
    data=data['fields']
    file=input("Enter output json file name like for hello.json ente hello \n")
    with open(file+".json", 'w') as f:
        json.dump(data, f)

#%%


else:
    file=input("Enter output json file name like for hello.json ente hello \n")
    with open(file+".json", 'w') as f:
        json.dump(log, f)

