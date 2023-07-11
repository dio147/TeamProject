import json

import requests
url = 'http://127.0.0.1:8000/regist/'
data = {'account': '123', 'password': '123'}
req = requests.post(url, data)
# rply = json.loads(req.text)
print(req)
