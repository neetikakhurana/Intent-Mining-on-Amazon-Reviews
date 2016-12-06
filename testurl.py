import requests
import json

url_put = 'http://localhost:5000/ReviewShilling/v1.0/products/7887421268'
url_post = 'http://localhost:5000/ReviewShilling/v1.0/products'

payload_put = json.loads(open('put.txt', 'rt').read())
payload_post = json.loads(open('new.txt', 'rt').read())

print(payload_put)
r = requests.put(url_put, auth=('sai', 'vallurupalli'), data=json.dumps(payload_put))
print(payload_post)
r = requests.post(url_post, auth=('sai', 'vallurupalli'), data=json.dumps(payload_post))
r = requests.delete(url_post + '/788742126N', auth=('sai', 'vallurupalli'), data=json.dumps(payload_post))

print(r.text)
print(r.status_code)
