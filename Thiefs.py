import os
import requests
import gspread
from google.oauth2.service_account import Credentials

# قراءة ملف Config.json موجود في نفس المجلد
SERVICE_ACCOUNT_FILE = 'Config.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

gc = gspread.authorize(credentials)

sheet_url = 'https://docs.google.com/spreadsheets/d/1MsnREiLwMupFv1JqFN1bApRyVeiC9GWahRxtcuyW5CU/edit#gid=0'
sh = gc.open_by_url(sheet_url)
worksheet = sh.sheet1

all_values = worksheet.get_all_values()
num_rows = len(all_values)
prev_num_file = 'prev_num.txt'
with open(prev_num_file, 'r') as f:
    prev_num = int(f.read().strip())
if num_rows > prev_num:
    bot_token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    message = f'There is a new Thief With Number: {num_rows}'
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    
    response = requests.post(url, data=payload)
    
    if response.status_code == 200:
        print("Message sent successfully!")
        with open(prev_num_file, 'w') as f:
            f.write(str(num_rows))
    else:
        print(f"Failed to send message: {response.text}")
    
else:
    bot_token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    message = f'There is a no Thiefs'
    
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
        'chat_id': chat_id,
        'text': message
    }
    
    response = requests.post(url, data=payload)
    
