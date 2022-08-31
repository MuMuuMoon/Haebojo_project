
############################# OPEN DIALOG
#-*- coding:utf-8 -*-
import urllib3
import json
 
openApiURL = "http://aiopen.etri.re.kr:8000/Dialog"
accessKey = "6051cf08-c45d-4b43-886c-1f63d31ebaa9"
access_method = "internal_data"
method = "open_dialog"
name = "DOMAIN_NAME"
 
requestJson = {
    "access_key": accessKey,
    "argument": {
        "name": name,
        "method": method,
        "access_method": access_method
    }
}
 
http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)
 
print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))
 
############################# DIALOG
#-*- coding:utf-8 -*-
import urllib3
import json
 
openApiURL = "http://aiopen.etri.re.kr:8000/Dialog"
accessKey = "6051cf08-c45d-4b43-886c-1f63d31ebaa9"
uuid = "UUID_FROM_OPEN_DIALOG"
text = "YOUR_TEXT"
method = "dialog"
 
requestJson = {
    "access_key": accessKey,
    "argument": {
        "method": method,
        "text": text,
        "uuid": uuid
    }
}
 
http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)
 
print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))