
#-*- coding:utf-8 -*-
import urllib3
import json
import base64
import re

def test(s):
    hangul = re.compile('[^ ㄱ-ㅣ가-힣+]') # 한글과 띄어쓰기를 제외한 모든 글자
    # hangul = re.compile('[^ \u3131-\u3163\uac00-\ud7a3]+')  # 위와 동일
    result = hangul.sub('', s) # 한글과 띄어쓰기를 제외한 모든 부분을 제거
    return(result)

openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
accessKey = "6051cf08-c45d-4b43-886c-1f63d31ebaa9"
audioFilePath = "./01_펩시_콜라_어딨어.wav"
languageCode = "korean"
 
file = open(audioFilePath, "rb")
audioContents = base64.b64encode(file.read()).decode("utf8")
file.close()
 
requestJson = {
    "access_key": accessKey,
    "argument": {
        "language_code": languageCode,
        "audio": audioContents
    }
}
 
http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8"},
    body=json.dumps(requestJson)
)
 
# print("[responseCode] " + str(response.status))
# print("[responBody]")
# print(str(response.data,"utf-8"))

# 문자열에서 한글만 추출하기
hangul = test(str(response.data,"utf-8"))
print(hangul)

# 한글 문장에서 안내해야 할 제품 이름 찾기
if "펩시" in hangul:
    print("펩시 콜라는 선반 1번째 칸 2번째에 있습니다.")