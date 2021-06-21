
import requests
from datetime import datetime
import time
import schedule

base_cowin_url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
now = datetime.now()
today_date = now.strftime("%d-%m-%Y")
api_url_telegram = "https://api.telegram.org/bot1812493768:AAE7HlpjHzQ5USUn-F4drRrrFo73SuSY9bM/sendMessage?chat_id=@__groupid__&text="
group_id = "vaccine_help"


def fetch_data_from_cowin(district_id):
    query_params = "?district_id={}&date={}".format(district_id, today_date)
    final_url = base_cowin_url + query_params
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
           'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
           'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
           'Accept-Encoding': 'none',
           'Accept-Language': 'en-US,en;q=0.8',
           'Connection': 'keep-alive'}

    response = requests.get(final_url, headers=hdr)
    extract_availabiltiy_data(response)


def extract_availabiltiy_data(response):
    response_json = response.json()
    for center in response_json["centers"]:
        message = ""
        for session in center["sessions"]:
            if session["available_capacity_dose1"] > 0 and session["min_age_limit"] == 18:
                message += "Pincode: {}\nName: {}\nSlot: {}\nDate: {}\nVaccine: {} \nFee Type: {}\nMinimum Age:{}\n ----- \n".format(
                    center["pincode"], center["name"],
                    session["available_capacity_dose1"],
                    session["date"],
                    session["vaccine"],
                    center["fee_type"],
                    session["min_age_limit"]
                )
        send_message_telegram(message)


def send_message_telegram(message):
    final_telegram_url = api_url_telegram.replace("__groupid__",  group_id)
    final_telegram_url = final_telegram_url + message
    response = requests.get(final_telegram_url)


if __name__ == "__main__":
    schedule.every(20).seconds.do(lambda: fetch_data_from_cowin(664))
    while True:
        schedule.run_pending()
        time.sleep(1)
