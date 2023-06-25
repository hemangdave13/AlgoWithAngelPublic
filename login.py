from smartapi import SmartConnect
import os
from pyotp import TOTP

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



