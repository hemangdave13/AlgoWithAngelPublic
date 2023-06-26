from smartapi import SmartConnect
import os
from pyotp import TOTP
import urllib
import json
import pandas as pd
import datetime as dt
key_path = r"/home/hemang/python/algo_trading/Angel_one/AlgoWithAngelPublic"

os.chdir(key_path)

key_secret = open("details.txt","r").read().split()

api_key = key_secret[0]
api_secret = key_secret[1]
client_id = key_secret[2]
password = key_secret[3];
totp = TOTP(key_secret[4]).now()
obj=SmartConnect(api_key=api_key)

#login api call

data = obj.generateSession(client_id,password,totp)

instruments_url = "https://margincalculator.angelbroking.com/OpenAPI_File/files/OpenAPIScripMaster.json"


response = urllib.request.urlopen(instruments_url);

instruments_list = json.loads(response.read())

# Function For get token from the ticker name 
def token_lookup(ticker,instruments_list,exchange= "NSE" ):
    for instrument in instruments_list:
        if(instrument["name"] == ticker and instrument["exch_seg"] == exchange and instrument['symbol'].split("-")[-1] == "EQ" ):
            return instrument["token"]
        
      

# Function For get ticker name from the token 
def symbol_lookup(token,instruments_list,exchange = "NSE"):
    for instrument in instruments_list:
        
        if(instrument["token"] == token and instrument["exch_seg"] == exchange and instrument['symbol'].split("-")[-1] == "EQ"):
            return instrument["name"]
       

#Function For get Historical Data 

def get_hist_data(ticker, duration, interval,instruments_list, exchange = "NSE"):
    params = {
     "exchange": exchange,
     "symboltoken": token_lookup(ticker,instruments_list,exchange),
     "interval": interval,
     "fromdate": (dt.date.today() - dt.timedelta(duration)).strftime("%Y-%m-%d %H:%M"),
     "todate": dt.date.today().strftime("%Y-%m-%d %H:%M")
     }
    hist_data = obj.getCandleData(params)
    #df_data = pd.DataFrame(hist_data['data'])
    df_data = pd.DataFrame(hist_data['data'],
                           columns = ["date","open","high","low","close","volumn"])
    df_data.set_index("date",inplace=True)
    return df_data

hdfc_data = get_hist_data("HDFC",30, "ONE_DAY", instruments_list)

print(hdfc_data)
    