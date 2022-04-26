from ast import For
import sys
import pyupbit
import time
from upbitpy import Upbitpy
import requests
import telegram
import math
#access = "HxHLPLB9rcmxWdgLZeZ7YgQe5bD62WByQxwSZG8l"          # 본인 값으로 변경
#secret = "dkWZxehSdcruJ1Gk5OxpvXAxfxxxVe6qO85mUXs6"          # 본인 값으로 변경
#upbit = pyupbit.Upbit(access, secret)

bot = telegram.Bot(token='5158038741:AAH0PRveNGIjqMRCeauhY8rJh3ZH6kUi2eo')
chat_id = -1001468635727
total_percent = 0
korean_name = ""
def process_start(ticker,koreanName):
    try:
        data_count = 5 # 5개 데이터만 추출
        now = pyupbit.get_current_price(ticker);
        num_str = str(round(now,2))
        print(ticker+" 시작")
                
        if ticker == "KRW-BTC" :
            df = pyupbit.get_ohlcv(ticker, "minute15", count=2)
            print(df)
            cent1 = cent_start(now,df['close'][1])
            #print("0")
            cent2 = cent_start(df['close'][1],df['close'][0])
            #print("1")
            total_cent = (cent1 + cent2)
            total_cent_str = str(round(total_cent, 2))
            #print("2")
            print("["+ticker+ "] 현재가격 : " + num_str + ",  " + total_cent_str + "% , 현재시간 : " + time.strftime('%m-%d %H:%M'))
            
            if total_cent < -0.5 :
                telegram_send(chat_id,"[비트코인-하락] 현재가격 : " + num_str + ",  " + total_cent_str + "%  https://upbit.com/exchange?code=CRIX.UPBIT."+ str(ticker) + "&tab=chart")
            elif  total_cent < -0.8 :
                telegram_send(chat_id,"[비트코인-큰하락] 현재가격 : " + num_str + ",  " + total_cent_str + "%  https://upbit.com/exchange?code=CRIX.UPBIT."+ str(ticker) + "&tab=chart")
            elif total_cent < -1.5 :
                telegram_send(chat_id,"[비트코인-대피해] 현재가격 : " + num_str + ",  " + total_cent_str + "%  https://upbit.com/exchange?code=CRIX.UPBIT."+ str(ticker) + "&tab=chart")
            elif total_cent > 0.4 :
                telegram_send(chat_id,"[비트코인-상승전환] 현재가격 : " + num_str + ",  " + total_cent_str + "%  https://upbit.com/exchange?code=CRIX.UPBIT."+ str(ticker) + "&tab=chart")
        elif ticker == "KRW-BTT" :
             print("예외")
        elif ticker == "KRW-XEC" :
             print("예외")
        else :
            df = pyupbit.get_ohlcv(ticker, "minute5", count=5)
            print(df)
            #print("1 0")
            cent1 = cent_start(now, df['close'][4])
            #print("1 1")
            cent2 = cent_start(df['close'][4], df['close'][3])
            #print("1 2")
            cent3 = cent_start(df['close'][3], df['close'][2])
            #print("1 3")
            num_str = str(round(now,2))
            #print("2")
            total_cent = (cent1 + cent2 + cent3)
            total_cent_str = str(round(total_cent, 2))
            #print("3")
            print("["+koreanName+ "] 현재가격 : " + num_str + ",  " + total_cent_str + "% , 현재시간 : " + time.strftime('%m-%d %H:%M'))
            
            if total_cent > 20 :
                telegram_send(chat_id,"["+koreanName+ "-100% 가즈아] 현재가격 : " + num_str + ",  " + total_cent_str + "%  https://upbit.com/exchange?code=CRIX.UPBIT."+ str(ticker) + "&tab=chart")
            elif total_cent > 10 :
                telegram_send(chat_id,"["+koreanName+ "-큰손왔다] 현재가격 : " + num_str + ",  " + total_cent_str + "%  https://upbit.com/exchange?code=CRIX.UPBIT."+ str(ticker) + "&tab=chart")
            elif  total_cent > 5 :
                telegram_send(chat_id,"["+koreanName+ "-큰상승] 현재가격 : " + num_str + ",  " + total_cent_str + "%  https://upbit.com/exchange?code=CRIX.UPBIT."+ str(ticker) + "&tab=chart")
            elif total_cent > 3  :
               telegram_send(chat_id,"["+koreanName+ "-상승] 현재가격 : " + num_str + ",  " + total_cent_str + "%  https://upbit.com/exchange?code=CRIX.UPBIT."+ str(ticker) + "&tab=chart")
            elif total_cent < -5 :
                telegram_send(chat_id,"["+koreanName+ "-큰하락] 현재가격 : " + num_str + ",  " + total_cent_str + "%  https://upbit.com/exchange?code=CRIX.UPBIT."+ str(ticker) + "&tab=chart")
    except:
        print("error")
        telegram_send(chat_id,"[원군봇 오류] " + ticker )


def cent_start(price, price2):
  
    try:
        #print("cent_start")
        compare_vol = (price-price2)
        persent =(compare_vol/price2*100)    
        return persent     
    except:
        print("error2")
        return 0  

def telegram_send(chat_id, text):
    try:
       bot.sendMessage(chat_id=chat_id, text=text)
       #print("send")
    except:
        print("error3")
        return 0  

#bot.sendMessage(chat_id=chat_id, text='[원군봇 시작]')
#tickers = pyupbit.get_tickers("KRW")
url = "https://api.upbit.com/v1/market/all?isDetails=true"
resp = requests.get(url)
tickers = resp.json()

while True:
    for ticker in tickers :
        if ticker["market"].startswith("KRW") : 
            process_start(ticker["market"],ticker["korean_name"])
            time.sleep(0.2)

    