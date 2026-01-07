#!/usr/bin/env python3
"""
Upbit Auto Trading Bot
모멘텀 기반 트레이딩 전략
"""

import os
import time
import pyupbit
import pandas as pd
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class UpbitTradingBot:
    def __init__(self):
        self.access = os.getenv('UPBIT_ACCESS_KEY')
        self.secret = os.getenv('UPBIT_SECRET_KEY')
        self.upbit = pyupbit.Upbit(self.access, self.secret)
        self.ticker = os.getenv('TRADING_COIN', 'KRW-BTC')
        self.buy_amount = int(os.getenv('BUY_AMOUNT', 5000))
        self.stop_loss = float(os.getenv('STOP_LOSS_PERCENT', 5)) / 100
        self.take_profit = float(os.getenv('TAKE_PROFIT_PERCENT', 10)) / 100
        
    def get_balance(self, ticker="KRW"):
        """잔고 조회"""
        balance = self.upbit.get_balance(ticker)
        return balance
    
    def get_current_price(self):
        """현재가 조회"""
        return pyupbit.get_orderbook(ticker=self.ticker)['orderbook_units'][0]['ask_price']
    
    def calculate_rsi(self, df, period=14):
        """RSI 계산"""
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_bollinger_bands(self, df, period=20, std=2):
        """볼린저 밴드 계산"""
        df['sma'] = df['close'].rolling(window=period).mean()
        df['std'] = df['close'].rolling(window=period).std()
        df['upper_band'] = df['sma'] + (df['std'] * std)
        df['lower_band'] = df['sma'] - (df['std'] * std)
        return df
    
    def check_buy_signal(self):
        """매수 시그널 확인"""
        try:
            df = pyupbit.get_ohlcv(self.ticker, interval="minute60", count=200)
            if df is None or len(df) < 60:
                return False
            
            # RSI 계산
            rsi = self.calculate_rsi(df)
            current_rsi = rsi.iloc[-1]
            
            # 볼린저 밴드 계산
            df = self.calculate_bollinger_bands(df)
            current_price = df['close'].iloc[-1]
            lower_band = df['lower_band'].iloc[-1]
            
            # 매수 조건: RSI < 30 (과매도) AND 가격이 하단 밴드 근처
            if current_rsi < 30 and current_price < lower_band * 1.02:
                print(f"[매수 시그널] RSI: {current_rsi:.2f}, Price: {current_price}, Lower Band: {lower_band:.2f}")
                return True
            
            return False
        except Exception as e:
            print(f"매수 시그널 확인 오류: {e}")
            return False
    
    def check_sell_signal(self, avg_buy_price):
        """매도 시그널 확인"""
        try:
            current_price = self.get_current_price()
            profit_rate = (current_price - avg_buy_price) / avg_buy_price
            
            # 손절 조건
            if profit_rate < -self.stop_loss:
                print(f"[손절] 손실률: {profit_rate*100:.2f}%")
                return True, "stop_loss"
            
            # 익절 조건
            if profit_rate > self.take_profit:
                print(f"[익절] 수익률: {profit_rate*100:.2f}%")
                return True, "take_profit"
            
            # RSI 기반 매도
            df = pyupbit.get_ohlcv(self.ticker, interval="minute60", count=200)
            if df is not None:
                rsi = self.calculate_rsi(df)
                current_rsi = rsi.iloc[-1]
                
                if current_rsi > 70 and profit_rate > 0.02:  # RSI 과매수 + 최소 2% 수익
                    print(f"[RSI 매도] RSI: {current_rsi:.2f}, 수익률: {profit_rate*100:.2f}%")
                    return True, "rsi_overbought"
            
            return False, None
        except Exception as e:
            print(f"매도 시그널 확인 오류: {e}")
            return False, None
    
    def buy_coin(self):
        """코인 매수"""
        try:
            krw_balance = self.get_balance("KRW")
            if krw_balance < self.buy_amount:
                print(f"잔고 부족: {krw_balance} KRW")
                return False
            
            result = self.upbit.buy_market_order(self.ticker, self.buy_amount)
            if result:
                print(f"[매수 완료] {self.ticker}, 금액: {self.buy_amount} KRW")
                return True
            return False
        except Exception as e:
            print(f"매수 오류: {e}")
            return False
    
    def sell_coin(self):
        """보유 코인 전량 매도"""
        try:
            coin_balance = self.get_balance(self.ticker.split('-')[1])
            if coin_balance <= 0:
                print("보유 코인 없음")
                return False
            
            result = self.upbit.sell_market_order(self.ticker, coin_balance)
            if result:
                print(f"[매도 완료] {self.ticker}, 수량: {coin_balance}")
                return True
            return False
        except Exception as e:
            print(f"매도 오류: {e}")
            return False
    
    def run(self):
        """봇 실행"""
        print(f"===== Upbit Trading Bot Started =====")
        print(f"Trading Coin: {self.ticker}")
        print(f"Buy Amount: {self.buy_amount} KRW")
        print(f"Stop Loss: {self.stop_loss*100}%")
        print(f"Take Profit: {self.take_profit*100}%")
        print(f"=====================================")
        
        while True:
            try:
                now = datetime.now()
                print(f"\n[{now.strftime('%Y-%m-%d %H:%M:%S')}] 상태 확인...")
                
                # 보유 코인 확인
                coin_ticker = self.ticker.split('-')[1]
                coin_balance = self.get_balance(coin_ticker)
                krw_balance = self.get_balance("KRW")
                
                print(f"보유 KRW: {krw_balance:.0f}, 보유 {coin_ticker}: {coin_balance:.8f}")
                
                if coin_balance > 0:
                    # 보유 중: 매도 시그널 확인
                    avg_buy_price = self.upbit.get_avg_buy_price(self.ticker)
                    current_price = self.get_current_price()
                    profit_rate = (current_price - avg_buy_price) / avg_buy_price * 100
                    
                    print(f"평균 매수가: {avg_buy_price:.0f}, 현재가: {current_price:.0f}, 수익률: {profit_rate:.2f}%")
                    
                    should_sell, reason = self.check_sell_signal(avg_buy_price)
                    if should_sell:
                        print(f"매도 이유: {reason}")
                        self.sell_coin()
                        time.sleep(2)
                else:
                    # 미보유: 매수 시그널 확인
                    if self.check_buy_signal():
                        self.buy_coin()
                        time.sleep(2)
                
                # 1분 대기
                time.sleep(60)
                
            except Exception as e:
                print(f"오류 발생: {e}")
                time.sleep(60)

if __name__ == "__main__":
    bot = UpbitTradingBot()
    bot.run()
