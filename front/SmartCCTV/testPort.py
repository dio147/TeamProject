
import requests
import json
import re
import base64
def myfuc():
    url = "http://127.0.0.1:8000/testget/"
    req = requests.get(url)
    ans = json.loads(req.text)['file']
    updateNum = json.loads(req.text)['update']
    print(updateNum)

    image_str= ans.encode('ascii')
    image_byte = base64.b64decode(image_str)
    image_json = open('afile.jpg', 'wb')
    image_json.write(image_byte)


def testpost():
    
    url = "http://127.0.0.1:8000/testpost/"
    req = requests.post(url,{'data':1})
    ans = json.loads(req.text)
    print(ans)

def test_daily():
    url="http://127.0.0.1:8000/student_daily/post/"

    req=requests.post(url,{'s20191571':json.dumps([20,30,40]),'s20191570':json.dumps([30,40,50])})
    ans=json.loads(req.text)
    print(ans)


if __name__ == '__main__':
    test_daily()