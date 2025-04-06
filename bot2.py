import requests
import time
import json
i=0
while(True):
  i+=1
  st = time.time()
  r = requests.patch('https://jqualin-990c1-default-rtdb.firebaseio.com/r.json',json={'i':i,'time':time.ctime()})
  print(time.time()-st)
  time.sleep(3)
time.sleep(10)
