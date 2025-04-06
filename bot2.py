import requests
import time
import json
r = requests.patch('https://jqualin-990c1-default-rtdb.firebaseio.com/r.json',json={'hi':'mf'})
print(r)
time.sleep(10)
