import os
import requests
import gspread
from google.oauth2.service_account import Credentials
from google.auth.exceptions import RefreshError
from gspread.exceptions import APIError


SERVICE_ACCOUNT_FILE = 'Config.json'

SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

try:
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

    prev_num_sheet_url = 'https://docs.google.com/spreadsheets/d/1ixe0S7_f0XKi7b6y8A6FhcI9GWwzqIZnxM_hUxDImd4/edit#gid=0'
    prev_num_sheet = gc.open_by_url(prev_num_sheet_url)
    prev_ws = prev_num_sheet.sheet1

    prev_num_cell = prev_ws.acell('A1').value
    prev_num = int(prev_num_cell) if prev_num_cell else 0

    if num_rows > prev_num:
        try:
            prev_ws.update('A1', [[str(num_rows)]])
            print("تم تحديث عدد الصفوف في الجدول الثاني.")

            # إرسال رسالة تيليجرام
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
            else:
                print(f"Failed to send message: {response.text}")

        except APIError as e:
            print("خطأ في تحديث الجدول:", e)
except:
    bot_token = os.environ.get('BOT_TOKEN')
    chat_id = os.environ.get('CHAT_ID')
    message = f'There is an Error go to check it '
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    payload = {
            'chat_id': chat_id,
            'text': message
        }
    response = requests.post(url, data=payload)

