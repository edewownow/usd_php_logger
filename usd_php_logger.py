import requests
import datetime
import csv
import os

LOG_FILE = "usd_php_bsp_log.csv"
import time
import requests

def get_usd_php_rate(max_retries=3, delay=5):
    url = "https://api.frankfurter.app/latest?from=USD&to=PHP"

    for attempt in range(1, max_retries + 1):
        try:
            print(f"Attempt {attempt} of {max_retries}...")
            response = requests.get(url, timeout=10)
            response.raise_for_status()  # catch HTTP errors

            data = response.json()
            return float(data["rates"]["PHP"])

        except Exception as e:
            print(f"Error: {e}")

            if attempt < max_retries:
                print(f"Retrying in {delay} seconds...")
                time.sleep(delay)
            else:
                raise  # rethrow after final attempt

def initialize_log():
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Date", "Time", "USD_to_PHP"])

def log_rate():
    try:
        rate = get_usd_php_rate()
    except Exception as e:
        with open("error_log.txt", "a", encoding="utf-8") as err:
            err.write(f"{datetime.datetime.now()} - ERROR: {str(e)}\n")
        return

    now = datetime.datetime.now()
    date_str = now.strftime("%Y-%m-%d")
    time_str = now.strftime("%H:%M:%S")

    with open(LOG_FILE, "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([date_str, time_str, rate])

    print(f"Logged: {date_str} {time_str} | USD to PHP: {rate}")

# MAIN EXECUTION
print("Script started")
initialize_log()
log_rate()