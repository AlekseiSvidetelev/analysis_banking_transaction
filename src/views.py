import requests
from dotenv import load_dotenv
import os


load_dotenv()
API_KEY = os.environ.get("API_KEY")

start_date = "2020-04-05" # 2020-04-05
end_date = "2020-05-04"
url = f"https://api.apilayer.com/exchangerates_data/timeseries?start_date={start_date}&end_date={end_date}"

payload = {}
headers= {
  "apikey": API_KEY
}

response = requests.request("GET", url, headers=headers, data = payload)

status_code = response.status_code
result = response.text
print(result)


