from requests import Session #to send HTTP requests to API
from twilio.rest import Client #to send SMS alert using TWILIO api
import json #to get data in json format
import time 
import html

CRYPTO_NAME = 'bitcoin' #Crypto you want to get alert of
ID = '1' #Crypto id you can get on Coinmarketcap.com
SYMBOL = 'BTC' #symbol of crypto
CURRENCY = '' #currency of your liking
NEWS_ENDPOINT = 'https://newsapi.org/v2/everything' #your choice  of News API endpoint Here I have used newsapi
NEWS_KEY = '' #your NEWS API Authentication key (you can get it by create acc)


NEWS_PARAMETER = {
    'q': CRYPTO_NAME,
    'apiKey': NEWS_KEY,

}

news_response = Session().get(NEWS_ENDPOINT, params=NEWS_PARAMETER)
news_response.raise_for_status()

news_data = news_response.json()
three_articles = news_data['articles'][:3] #you can change number of articles accounding to you preferences

#after creating acc on twilio you get your own account id and token
account_sid = ''
auth_token = ''

CRYPTO_ENDPOINT = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest' #your choice of CRYPTO API endpoint Here I have  used coinmarketcap
CRYPTO_PARAMS = {
  'slug': CRYPTO_NAME,
  'convert': CURRENCY

}
headers = {
  'Accepts': 'application/json',
  'X-CMC_PRO_API_KEY': '' #your CRYPTO API Authentication key (you can get it by create acc),
}

session = Session()
session.headers.update(headers)

price_alert_on = False
while not price_alert_on:
    response = session.get(CRYPTO_ENDPOINT, params=CRYPTO_PARAMS)
    data = json.loads(response.text)
    price = "%.2f"%(data["data"][ID]['quote']['INR']['price'])
    one_hour_diff_percent = float('%.2f'%(data["data"][ID]['quote'][CURRENCY]['percent_change_1h']))
    up_down = None
    if float(one_hour_diff_percent) > 0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    formatted_article = [f"{CRYPTO_NAME}: {up_down}{one_hour_diff_percent}% \nHeadline: {article['title']}." \
                         f" \nBrief: {article['description']}" for article in three_articles]

    if abs(one_hour_diff_percent) > 5 or abs(one_hour_diff_percent) < 5:
        client = Client(account_sid, auth_token)

        for article in formatted_article:
            article = html.unescape(article)
            message = client.messages.create(
                body=article,
                from_='', #your own Twilio number you get after creating acc,
                to="" #phone number you want to get SMS alert on
            )
    time.sleep(3600)
    

# NOTE:
#           TO get SMS alert every HOUR 
#           1. you have to create acc on https://www.pythonanywhere.com.
#           2. Upload this file (main.py) in Files section.
#           3. After uploading double tab main.py and open bash console.
#           4. In bash console type 'Python3 main.py' to run your code.
#           5. Then move to the task section and set time according to your country timeline and in text box type 'Python3 main.py'
#           6. Press Create.
#           7. Now you will recieve SMS alert every 1 hour  if price goes up by 5% or down by 5% on your suggested time.
