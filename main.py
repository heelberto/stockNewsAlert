import requests
import datetime
import json
import math
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
ALPHA_VANTAGE_API_KEY = "IF85YSFI9Z3CFIQV"
NEWS_API_KEY = "44d3c70a242547d7be65a0b108d9d0a1"
TWILIO_ACCOUNT_SID = "ACaf49bc2422137739a106212f8e63b230"
AUTH_TOKEN = "f25c90f106c2d3d82b0a717b1dc25cf8"
client = Client(TWILIO_ACCOUNT_SID, AUTH_TOKEN)

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"


def get_news(stockPercentageChange):
    """
    Fetches news related to the specified stock and sends it via SMS using Twilio.

    Args:
    - stockPercentageChange (float): Percentage change in the stock price.
    """
    # make API call and parse data
    response = requests.get(url=f"https://newsapi.org/v2/top-headlines?q=tesla&apiKey={NEWS_API_KEY}")
    response.raise_for_status()
    data = response.json()
    top_three_articles = data["articles"][0:3]
    message = f"{stockPercentageChange} % change in TSLA stock\n"
    for article in top_three_articles:
        message += f"Headline: {article['title']}\nBrief: {article['description']}\nLink: {article['url']}\n"

    #print(message)
    txt_message = client.messages.create(
        from_='+18444640179',
        body=f'{message}',
        to='+17147078504'
    )


def stock_change(new_price, old_price):
    """
     Calculates percentage change in stock price.
    Args:
    - new_price (float): New closing price of the stock.
    - old_price (float): Previous day's closing price of the stock.

    Returns:
    - float: Percentage change in stock price.
    """
    return ((new_price-old_price)/old_price) * 100

# get daily stock data from previous 5 months
def stock_check():

    """
    Checks daily stock price change and sends news if the change is significant
    """
    # make API call and parse data
    # response = requests.get(url=f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={STOCK_NAME}&outputsize=compact&apikey={ALPHA_VANTAGE_API_KEY}")
    # response.raise_for_status()
    # print(response.status_code)
    # data = response.json()


    # read data from data.txt, in order to debug and not wast #of daily API calls
    data = ""
    with open("data.txt", "r") as file:
        data = file.read()

    # convert the data to a dictionary for ease of use
    data_dict = json.loads(data.replace("'", '"'))

    # determine correct dates
    yesterday_date = str(datetime.datetime.now().date() - datetime.timedelta(days=4))
    day_b4_yesterday_date = str(datetime.datetime.now().date() - datetime.timedelta(days=5))

    # determine closing values
    yesterday_close = float(data_dict["Time Series (Daily)"][f"{yesterday_date}"]["4. close"])
    day_b4_yesterday_close = float(data_dict["Time Series (Daily)"][f"{day_b4_yesterday_date}"]["4. close"])

    stock_change_percentage = stock_change(yesterday_close, day_b4_yesterday_close)

    # determine if the difference in closing values is +/-
    if abs(stock_change(yesterday_close, day_b4_yesterday_close)) > 5:
        get_news(f"{stock_change_percentage:.2f}")


stock_check()
