#%%
import splunklib.client as client
import splunklib.results as results
import io
import pandas as pd
import urllib.request
import json
import copy
#%%
#  splunk command : host="check"| stats values as * by name
def send_event(splunk_host, auth_token, log_data,hostid):
   
   try:
      
      host_id = hostid
      source_type = "_json"      
      request_url = "http://%s:8088/services/collector" % splunk_host      
      post_data = {
         
         "host": host_id,
         "sourcetype": source_type,
         "event": log_data
      }      
      data = json.dumps(post_data).encode('utf8')      
      auth_header = "Splunk %s" % auth_token
      headers = {'Authorization' : auth_header}       
      req = urllib.request.Request(request_url, data, headers)
      response = urllib.request.urlopen(req)      
      read_response = response.read()
      
      try:
         response_json = json.loads(str(read_response)[2:-1])         
         if "text" in response_json:
            if response_json["text"] == "Success":
               post_success = True
            else:
               post_success = False
      except:
         post_success = False
      
      if post_success == True:
         # Event was recieved successfully
         print ("Event was recieved successfully")
      else:
         # Event returned an error
         print ("Error sending request.")
      
   except Exception as err:
      # Network or connection error
      post_success = False
      print ("Error sending request")
      print (str(err))

   return post_success
#%%
def main(log_data,hostid):
   #splunk_auth_token = "6897dad5-11a8-420a-a63a-ac8d1b6ed019"
   splunk_auth_token = "c6b48f4a-b178-4387-aea4-b7f1c224424e"
   splunk_host = "localhost"   
   result = send_event(splunk_host, splunk_auth_token, log_data,hostid)
   print (result)

#%%
def uploadData():
    file=input("Enter avro file name with path (with extension like 'file.avsc') : ")
    f=open(file)
    j=json.load(f)
    log=j['fields']
    count=0
    for row in log:
        if 'name' not in row:
            break
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
        log=data

    hostid=input("Assign host_id : \n")
    main(log,hostid)
    return
#%%
def getData():
    user=input("enter splunk username : \n ")
    passwd=input("enter splunk password : \n")
    hostname=input("enter hostname (for local splunk enterprise type localhost) : \n")
    search_host=input("Enter host_id for search : \n")
    search_host="\""+search_host+"\""
    print("WARNING !! if using local splunk enterprise then set truncate=0 in props.conf file \n")
    service = client.connect(
                        host=hostname,
                        port=8089,
                        username=user,
                        password=passwd)    
    search_string = """ search host="""+search_host+ """|stats values as * by name  """
    job = service.jobs.create(search_string, **{"latest_time": "now",
                                                "earliest_time": "-5min",
                                                "exec_mode": "blocking" ,
                                                "count": 0})
    search_results = job.results(**{"output_mode": "csv"})
    res = search_results.read()
    first = True
    df = None
    s = io.StringIO(str(res.decode('utf8')))
    res_df = pd.read_csv(s, delimiter=',')
    if first:
                df = res_df
                first = False
    else:
        df = df.append(res_df, ignore_index=True)    
    df = df.replace(r'\x00','',regex=False)
    df = df.replace('\n',' ',regex=True)
    df = df.replace('\r',' ',regex=True)
    df = df.replace('\t',' ',regex=True)
    wname=input("Enter file name to be saved (with exetension like output.csv) : ")
    df.to_csv(wname, index=False)
    return
#%%
uploadData()
print("Data Uploaded !!")
getData()
#%%



    
    
