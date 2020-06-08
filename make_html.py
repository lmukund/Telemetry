import pandas as pd
import numpy as np
import random
import webbrowser
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
def readData():
    file = input("Enter file name with path (like C:\\data.csv) : \n")
    data=pd.read_csv(file)
    return data.iloc[:,:].values
#%%
def getKeyValue(item):
    item=item.split("==>")       
    key=item[0] 
    value=item[1]
    value_list=value.split("&")
    if len(value_list) > 1:
        value_list.sort()
        value='&'.join(value_list)
    return key,value,value_list
    
#%%
def mapTable(table):
    mapped_table={}
    ver_map={}
    releases=[]
    for key in table:
        li=table[key]
        min_dict=[]
        for item in li:
            min_key,min_value,versions=getKeyValue(item)
            min_dict.append([min_key,min_value])
            ver_map[min_value]=1
            releases=np.concatenate((releases,versions))
        mapped_table[key]=min_dict
    releases=list(dict.fromkeys(releases))
    return mapped_table,np.array(releases),ver_map
#%%
def assignColorNumber(verMap):
    index=1
    noToVer={}
    for key in verMap:
        verMap[key]="color_"+str(index)
        noToVer[index]=key
        index=index+1
    return verMap

#%%
def colorMap(ver_map):
    color_array=['#db736b',
                 '#8f5854',
                 '#6e6666',
                 '#a69567',
                 '#ba983c',
                 '#614700',
                 '#95a13f',
                 '#53b800',
                 '#698255',
                 '#7a7d78',
                 '#50ad83',
                 '#009653',
                 '#5067a6',
                 '#22366b',
                 '#8c5c9c',
                 '#915383',
                 '#bd3c7d',
                 '#260315']
    random.shuffle(color_array)
    color_noToCode={}
    ind=0
    for key in ver_map:
        color=ver_map[key]
        color_noToCode[color]=color_array[ind]
        ind=ind+1
    return color_noToCode       
        
          
#%%
def makeHTMLtable(table,ver_map):
    
    colorscheme="""<div class="btn-group">"""
    string=""
    for ver in ver_map:
        text=ver
        classname=ver_map[ver]
        string=string+"""\n <button type="button" class="btn """
        string=string+classname+"\"> "+text+" </button> \n"
    colorscheme=colorscheme+string+"</div>"   
    
    
    code="""<html>
<head>
	<link rel="stylesheet" href="style.css">	
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
</head>
<body><div class="jumbotron"> <h1> ISE Telemetry attributes </h1><h4>Color Scheme for version(s) :</h4> """+colorscheme+"""</div><table class="table table-bordered">"""
    for key in table:
        start="<tr><th>"+key+"</th><td><ul>"
        end="</ul></td></tr>"
        body=""
        
        li=table[key]
        for item in li:
            text=item[0]
            version=item[1]
            classname=ver_map[version]
            string="""<li class="list-group-item list-group-item-light">
            <div class="btn-group"><button type="button" class="btn """
            string=string+classname+"\">"+text+"""</button><button type="button" class="btn """
            string=string+classname+"\">"+version+"</button></div></li>"            
            body=body+string
        code=code+start+body+end
    close="""</table></body></html>"""
    code=code+close
    return code
    
def makeCSS(colors):
    head="""ul {
  list-style-type: square;
  list-style-position: outside;
  list-style-image: none;
}

table, th, td {
  border: 0.5px grey;
  table-layout: auto;
  width: 250px;
  border-top-right-radius: 20px;
  border-spacing: 5px;
}
th, td {
  padding: 15px;
  text-align: left;
}"""
    for classname in colors:
        string="\n ."+classname+" { background-color:"+colors[classname]+";\ncolor: white;\nmargin-right: 2px;\n}"
        head=head+string
    return head        
#%%    
def main():
    data=readData()
    table=makeTable(data)    
    mapped_table,releases,ver_map=mapTable(table)
    ver_map=assignColorNumber(ver_map)
    colors=colorMap(ver_map)
    html=makeHTMLtable(mapped_table,ver_map)
    css=makeCSS(colors)
    return html,css
#%%
html,css=main()
f1 = open('table.html','w')
f1.write(html)
f1.close()
f2 = open('style.css','w')
f2.write(css)
f2.close()
webbrowser.open_new_tab('table.html')
#%%























