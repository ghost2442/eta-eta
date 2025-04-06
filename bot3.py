from telethon import TelegramClient

try:
  c = TelegramClient(None,'262663','jdjdieie98888')
  c.connect()
  print('connected')
except Exception as e:
  print(e)
