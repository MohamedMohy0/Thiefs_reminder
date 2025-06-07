import requests
import gspread
from google.oauth2.service_account import Credentials

# Your local JSON file path
SERVICE_ACCOUNT_FILE = 'Config.json'

SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']

# Authenticate with Google Sheets API
credentials = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=SCOPES
)

gc = gspread.authorize(credentials)

# Open your Google Sheet by URL or by name
sheet_url = 'https://docs.google.com/spreadsheets/d/1MsnREiLwMupFv1JqFN1bApRyVeiC9GWahRxtcuyW5CU/edit#gid=0'
sh = gc.open_by_url(sheet_url)

worksheet = sh.sheet1  # Get the first worksheet

all_values = worksheet.get_all_values()
num_rows = len(all_values)

bot_token = '8124295808:AAHZzbmfpRntxSFVZMAEfLyve8PfaP8EU48'
chat_id = '1752719138'
message = f'There is a new Thief With Number:{num_rows}'

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
