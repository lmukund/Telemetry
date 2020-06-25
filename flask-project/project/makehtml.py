
import pandas as pd
import numpy as np
import random
# %%


def readData():
    print("fetching data")
    file = "flaskdb.csv"
    data = pd.read_csv(file)
    data = data.iloc[:, :].values
    newdata = []
    special = []
    for item in data:
        if type(item[0]) == float:
            continue
        if type(item[1]) == float:
            special.append(item[0])
            continue
        newdata.append(np.array(item))
    table = {}
    for row in newdata:
        key = row[0]
        value = row[1:]
        if key not in table:
            if type(value[0]) == float:
                table[key] = []
            else:
                table[key] = [row[1:]]
        else:
            li = table[key]
            li.append(row[1:])
            table[key] = li
    newtable = {}
    for key in table:
        li = table[key]
        string = ""
        for item in li:
            attribute = item[0]
            version = item[1]
            if type(item[2]) == float:
                des = "No Information Available Yet"
            else:
                des = item[2]
            if type(version) != str:
                version = str(version)
            string = string+attribute+"==>"+version+"==>"+des+","
        newtable[key] = string
    for key in special:
        if key not in newtable:
            newtable[key] = []
    return newtable


# %%
def makeTable(data):
    table = {}
    for key in data:
        valueList = data[key]
        if type(valueList) != str:
            table[key] = []
            continue
        li = valueList.split(",")
        li = li[:-1]
        table[key] = li
    return table

# %%


def getKeyValue(item):
    item = item.split("==>")
    key = item[0]
    value = item[1]
    value_list = value.split("&")
    if len(value_list) > 1:
        value_list.sort()
        value = '&'.join(value_list)
    return key, value, item[-1], value_list

# %%


def mapTable(table):
    mapped_table = {}
    ver_map = {}
    releases = []
    for key in table:
        li = table[key]
        min_dict = []
        for item in li:
            min_key, min_value, min_des, versions = getKeyValue(item)
            min_dict.append([min_key, min_value, min_des])
            ver_map[min_value] = 1
            releases = np.concatenate((releases, versions))
        mapped_table[key] = min_dict
    releases = list(dict.fromkeys(releases))
    return mapped_table, np.array(releases), ver_map
# %%


def assignColorNumber(verMap):
    index = 1
    noToVer = {}
    for key in verMap:
        verMap[key] = "color_"+str(index)
        noToVer[index] = key
        index = index+1
    return verMap

# %%


def colorMap(ver_map):
    color_array = ['#db736b',
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
    color_noToCode = {}
    ind = 0
    for key in ver_map:
        color = ver_map[key]
        color_noToCode[color] = color_array[ind]
        ind = ind+1
    return color_noToCode


# %%
def makeHTMLtable(table, ver_map, black_list, css):

    colorscheme = """<div class="btn-group">"""
    string = ""
    for ver in ver_map:
        text = ver
        classname = ver_map[ver]
        string = string+"""\n <button type="submit" class="btn """
        string = string+classname+"\"> "+text+" </button> \n"
    colorscheme = colorscheme+string+"</div>"

    code = """<html><head><title>ISE Telemetry Attributes</title><style>"""+css+"""
    </style><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0/css/bootstrap.min.css" integrity="sha384-Gn5384xqQ1aoWXA+058RXPxPg6fy4IWvTNh0E263XmFcJlSAwiGgFAW/dAiS6JXm" crossorigin="anonymous">
    <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
</head>
<body>
    <div>
        {% with messages = get_flashed_messages(with_categories=true) %} {% if messages %} {% for category,msg in messages %}
        <div class="alert alert-{{ category }}">{{msg}}</div>
        {% endfor %} {% endif %} {% endwith %}
    </div>
   
    <div class="jumbotron">
        <h1> ISE Telemetry Attributes </h1>        
        <h4>Color Scheme for version(s) :</h4> """
    code = code+colorscheme + """
    <div class="instructions"> 
                <h4><br>INSTRUCTIONS : </h4>
                    <ol>           
                        <li>Hover over field for Description</li>
                        <li>Click on Edit to edit the Hovering Description</li>
                        <li>Click on Hide to remove the entry from showing on the page</li>
                    </ol>
                
    </div></div>
    <div class="edit-btn1"><a class="btn btn-outline-dark" href="{{ url_for('download_all') }}"> Download DBs (.zip) </a></div>
    <div class="edit-btn2"><a class="btn btn-outline-dark" href="{{ url_for('upload_file') }}"> Upload DB </a></div>
    <div class="container"><table class="table table-bordered">"""
    for key in table:
        start = "<tr><th>"+key+"</th><td><ul>"
        end = "</ul></td></tr>"
        body = ""

        li = table[key]
        for item in li:
            text = item[0]
            version = item[1]
            classname = ver_map[version]
            titletxt = item[2]
            info=key+" "+text
            string = """<li class="list-group-item list-group-item-light">
            <div class="btn-group"><button  type="button" class="btn """
            string = string+classname+"\" style=\"font-size:115%\" title=\""+titletxt+"\">" + \
                text+"""</button></a><button type="button" class="btn """
            string = string+classname + \
                "\" title=\"ISE Verion(s)\">"+version+"""</button></div>
                    <div style="float: right;" class="edit-form"><form method="post" action="/try" class="inline">
                    <input type="hidden" name="information" value=""" +"\""+info+"\""+ """>
                    <button type="submit" class="btn btn-light">Edit</button>
                    </form></div>
                    <div style="float: right;" class="edit-form"><form method="post" action="/hide" class="inline">
                    <input type="hidden" name="information" value=""" +"\""+info+"\""+ """>
                    <button type="submit" class="btn btn-light">Hide</button>
                    </form></div>
                </li>"""
            if text in black_list:
                string = "<!--"+string+"-->"
            body = body+string

        code = code+start+body+end
    close = """</table></div></body></html>"""
    code = code+close
    return code


def makeCSS(colors):
    head = """ul {
  list-style-type: square;
  list-style-position: outside;
  list-style-image: none;
}
.edit-head{
    position:absolute;
    top:4.72rem; 
    right:11.8rem;
}
.instructions{
    position:relative;
    
}
.btn-light {
    align:right;
    color: Red;
}
.head-group{
    position:absolute;    
}
title{
    font-size: large;
}
.title{
    font-size: large;
}

.edit-btn1{
    position:absolute;
    top:9.44rem; 
    right:9.8rem;
}
.edit-btn2{
    position:absolute;
    top:9.44rem; 
    right:2.36rem;
}
.btn btn-outline-dark{
    margin:2px;
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
        string = "\n ."+classname + \
            " { background-color:"+colors[classname] + \
            ";\ncolor: white;\nmargin-right: 2px;\n}"
        string=string+"\n ."+classname+":hover { font-size: 125%;}"
        head = head+string
    return head
# %%


def blacklist():
    string = input("Enter fields (cases sensitive and comma separated ,for eg:'Node,FIPSSTatus,null,Node_51') that you want to comment out in html OR press ENTER to skip : \n ")
    li = string.split(",")
    li = list(dict.fromkeys(li))
    return li


# %%
""" def main():
    data=readData()
    table=makeTable(data)    
    mapped_table,releases,ver_map=mapTable(table)
    #rekeases contains all the versions present
    ver_map=assignColorNumber(ver_map)
    colors=colorMap(ver_map)
    black_list=blacklist()
    html=makeHTMLtable(mapped_table,ver_map,black_list)
    css=makeCSS(colors)
    return html,css
"""
""" html,css=main()
f1 = open('table.html','w')
f1.write(html)
f1.close()
f2 = open('style.css','w')
f2.write(css)
f2.close()
webbrowser.open_new_tab('table.html')
 """
# %%
