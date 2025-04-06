import requests
import time
import json
i=0
ranfor=0
sttime=time.time()
while(True):
  i+=1
  st = time.time()
  ranfor=time.time()-sttime
  r = requests.patch('https://jqualin-990c1-default-rtdb.firebaseio.com/r.json',json={'i':i,'time':time.ctime(),'ranfor':ranfor})
  #print(time.time()-st)
  if ranfor>=10600:
    break
  time.sleep(3)
