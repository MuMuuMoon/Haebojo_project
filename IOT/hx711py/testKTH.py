import requests

datas={
    'key':'0'
    ,'key2' : '565'
    ,'key3' : '219'
}
print(type(datas))
url="http://192.168.123.3:5555/fromLoadcell"

response = requests.post(url, data=datas)
print(response.status_code)