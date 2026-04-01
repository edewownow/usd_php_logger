import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# -----------------------------
# Google Sheets Authentication
# -----------------------------
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("credentials.json", scopes=SCOPES)
client = gspread.authorize(creds)

# Open your sheet by name
SHEET_NAME = "usd_php_logs"
sheet = client.open(SHEET_NAME).sheet1

# -----------------------------
# Fetch USD → PHP rate
# -----------------------------
def get_usd_php_rate():
    url = "https://api.exchangerate-api.com/v4/latest/USD"
    response = requests.get(url)
    data = response.json()
    return data["rates"]["PHP"]

# -----------------------------
# Main logging function
# -----------------------------
def log_rate():
    try:
        rate = get_usd_php_rate()
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # Append row to Google Sheet
        sheet.append_row([timestamp, rate])

        print(f"Logged: {timestamp} | USD to PHP: {rate}")

    except Exception as e:
        print("Error:", e)

# Run the logger
if __name__ == "__main__":
    log_rate()
