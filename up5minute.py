import sys
import pyupbit
import time
from upbitpy import Upbitpy
from PyQt5.QtWidgets import *
from upbitpy import Upbitpy
import requests
import telegram
import math
#access = "HxHLPLB9rcmxWdgLZeZ7YgQe5bD62WByQxwSZG8l"          # 본인 값으로 변경
#secret = "dkWZxehSdcruJ1Gk5OxpvXAxfxxxVe6qO85mUXs6"          # 본인 값으로 변경
#upbit = pyupbit.Upbit(access, secret)



bot = telegram.Bot(token='5010813220:AAE6tmzwXz0EHhSY_8BR0SIArmYOru3c-IM')
chat_id = -1001553463477



krw_market_list = []
krw_market_listname = ""
krw_market_acc_list = []
krw_market_list_str = ""


url = "https://api.upbit.com/v1/market/all?isDetails=true"
resp = requests.get(url)
ticks = resp.json()
#print(ticks['korean_name'])
for tick in ticks:
    val="KRW-" in tick["market"]
    if val:
    
     #print(tick["market"][4:])
     krw_market_list_str +=tick["market"]+","
     #print(krw_market_list_str)
     krw_market_list.append(tick["market"][4:]);
     krw_market_listname +=tick["korean_name"]+","
#print(pyupbit.get_tickers(fiat="KRW"))

suz=len(krw_market_list_str)
suz=suz-1
krw_market_list_str.strip()
krw_market_list_str = krw_market_list_str[0:suz]
#print(krw_market_list_str)
cur_befor_acc_list = [];
before_acc_list = [];
cur_acc_list = [];

while True:
    try:
       
        cloud_data = [];
        min_acc_list = [];
        krw_market_list = [];
        upbit = Upbitpy()
        datalist = krw_market_list_str.split(",")
        namelist = krw_market_listname.split(",")
        all_info = upbit.get_ticker(datalist)
        #print(all_info)
        #print('len(all_info): ' +str(len(all_info)))    
        # url = "https://api.upbit.com/v1/ticker?markets="+krw_market_list_str
        # resp = requests.get(url)
        # tickers = resp.json()
        
        for idx,ticker in enumerate(all_info):
     
                #(뒤-앞)/앞*100
                #print(pyupbit.get_ohlcv(ticker['market'], interval="minute1", count=3))
                #closePrice =pyupbit.get_ohlcv(ticker['market'], interval="minute1", count=3)
                #print(closePrice)
                #closePrice =upbit.get_minutes_candles(1, ticker['market'], count=3)
                closePrice5 =upbit.get_minutes_candles(5, ticker['market'], count=4)
  
                
                rate = closePrice5[0]['trade_price']
                rate_one = closePrice5[1]['trade_price']
                rate_two = closePrice5[2]['trade_price']
                # print('현재rate: ' + str(rate))
                # print('1분전rate: ' + str(rate_one))
                # print('2분전rate: ' + str(rate_two))
                changeRate= round(ticker['signed_change_rate']*10000)/100
                # if "KRW-FCT2" == ticker['market']:
                    # print('----리플 거래량-----')
                change = ticker['change']
                korname = namelist[idx]
                if len(before_acc_list)<len(datalist) and len(cur_acc_list)==0:
                    before_acc_list.append(changeRate)
                    print('----before 거래량-----'+str(len(before_acc_list)))
                elif len(cur_befor_acc_list)<len(datalist) and len(before_acc_list)==len(datalist):
                    cur_befor_acc_list.append(changeRate)
                    print('----cur_befor 거래량-2----')
                else:
                    
                    ele2=before_acc_list[idx]
                    ele1=cur_befor_acc_list[idx]
                    cur_acc_list.append(changeRate)
                    result1=ele1+1.5
                    result2=ele2+1.5
                    percent_rising='-'
                    print('korname=='+str(korname))
                    print('ele1=='+str(ele1))
                    print('ele2=='+str(ele2))
                    print('changeRate=='+str(changeRate))
                    print('result1=='+str(result1))
                    print('result2=='+str(result2))
                    print('trade_time_kst=='+str(ticker['trade_date_kst']+ticker['trade_time_kst']))
                    print('========================================================================')
                    if (changeRate > result1 and change=='RISE') or (changeRate >result1 and result1 > result2): 
                        percent_rising='전일대비 변화'
                        changetxt = str(closePrice5[0]['candle_date_time_kst'])+'==('+str(korname)+')=='+percent_rising+'==▲=='+str(changeRate)+'==▲=='+change+'==https://api.upbit.com/v1/ticker?markets='+ticker['market']
                        bot.sendMessage(chat_id=chat_id, text=changetxt)
                        print('changetxt=='+str(changetxt))
                    if idx==109:
                        before_acc_list.clear
                        before_acc_list=cur_befor_acc_list
                        cur_befor_acc_list.clear
                        cur_befor_acc_list=cur_acc_list
                        cur_acc_list.clear

                    # print('korname=='+str(korname))
                    # print('ele1=='+str(ele1))
                    # print('ele2=='+str(ele2))
                    # print('changeRate=='+str(changeRate))
                    # print('trade_time_kst=='+str(ticker['trade_date_kst']+ticker['trade_time_kst']))
                    
                    # print('rate_one=='+str(rate_one))
                    # print('rate_two=='+str(rate_two))
                    before_acc_list[idx]
                
                
                rate5 = closePrice5[0]['trade_price']
                rate5_one = closePrice5[1]['trade_price']
                rate5_two = closePrice5[2]['trade_price']
                rate5_three = closePrice5[3]['trade_price']
                rate5_rising='-'
                change5_rate=0.0
               
               
                re=(rate5_three+rate5_one+rate5_two)/3
                change5_rate= round((rate5 - rate5_one) / rate5_one * 100,2)
                print('korname=='+str(korname)+'==▲=='+str(change5_rate))
                #(전 5분봉가격+ 전전5분봉 가격+ 전전전 5분봉 가격 / 3 ) x 1.05 <= 현재5분봉가격
                if ((rate5_three+rate5_one+rate5_two)/3*1.05)<=rate5:
                    
                    change5_rate= round((rate5 - rate5_one) / rate5_one * 100,2)
                    rate5_rising='상승기류포착'+change5_rate+'퍼상승'
                    #print('퍼센트: '+str(ticker['market'])+'('+str(korname)+')=='+rate5_rising+'==▲=='+str(change5_rate))
                    # print('1==='+str(re))
                    # print('2==='+str(rate5))
                    ratingtxt5 = str(ticker['market'])+'('+str(korname)+')==▲=='+rate5_rising
                    # print('현재: ' + str(closePrice5[0]['trade_price'])+'=='+str(rate5))
                    # print('10분전: ' + str(closePrice5[1]['trade_price'])+'=='+str(rate5_one))
                    # print('15분전: ' + str(closePrice5[2]['trade_price'])+'=='+str(rate5_two))
                    # print('20분전: ' + str(closePrice5[2]['trade_price'])+'=='+str(rate5_three))
                    bot.sendMessage(chat_id=chat_id, text=ratingtxt5)
                
                last = closePrice5[0]['candle_acc_trade_volume']
                last_one = closePrice5[1]['candle_acc_trade_volume']
                last_two = closePrice5[2]['candle_acc_trade_volume']
                last_three = closePrice5[2]['candle_acc_trade_volume']
                   
                volume_rising = '-'
                volume_change_rate = 0.0
                if ((last_one+last_two+last_three)/3*1.4)<=last and change5_rate>2.5:
                    volume_rising = '거래량급증'
                    volume_change_rate = (last - last_one) / last_one * 100
                    volumetxt =str(ticker['market'])+'('+str(korname)+')=='+volume_rising+'==▲=='+str(volume_change_rate)
                    print('거래량: '+str(ticker['market'])+'('+str(korname)+')=='+volume_rising+'==▲=='+str(volume_change_rate))
                    bot.sendMessage(chat_id=chat_id, text=volumetxt)
                time.sleep(1) 
        

    except Exception as e:
        print(e)
        time.sleep(1)