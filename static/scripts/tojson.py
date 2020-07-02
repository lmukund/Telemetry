
import json
file=input("Enter avro file name with path (with extension like 'file.avsc') : ")
f=open(file)
j=json.load(f)
log=j['fields']
file=input("Enter output json file name like for hello.json ente hello \n")
with open(file+".json", 'w') as f:
    json.dump(j, f)

