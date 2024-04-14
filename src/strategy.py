import talib as ta
import pandas as pd
from enum import Enum
from utils import adjust_price, adjust_qty

class Signal(Enum):
    ON = 1
    OFF = 0

class Strategy:
    def __init__(self, exchange, config):
        self.exchange = exchange
        self.pair_symbol = config['pair_symbol']
        self.trading_volume = float(config['trading_volume'])
        self.max_leverage = config['leverage'] if type(config['leverage']) == str else str(config['leverage'])
        self.interval = config['interval']
        self.num_candles = int(config['num_candles'])

        self.position = None
        self.orders = None
        self.symbol_info = {}

    async def initalize_setting(self):
        # cancel all existing orders
        await self.exchange.cancel_all_orders(self.pair_symbol)

        # set leverage
        ret_msg = await self.exchange.set_leverage(self.pair_symbol, self.max_leverage)
        if ret_msg == 'OK':
            print(f'[TradingStrategy]-initalize_setting: leverage is set to {self.max_leverage}x')
        elif ret_msg == 'leverage not modified':
            print(f'[TradingStrategy]-initalize_setting: leverage is already {self.max_leverage}x')
        else:
            print(f'[TradingStrategy]-initalize_setting: {ret_msg}')

        balance_info = await self.exchange.get_balance_info('USDT')
        usdt_balance = float(balance_info[0]['coin'][0]['availableToWithdraw'])
        print('[TradingStrategy]-initalize_setting:', usdt_balance)

        self.trading_volume = min(self.trading_volume, usdt_balance * int(self.max_leverage)) * 0.95
        print(f'[TradingStrategy]-initalize_setting: trading_volume is set to {self.trading_volume}')

        price_tick, qty_step = await self.exchange.get_symbol_info(self.pair_symbol)
        self.symbol_info = {'price_tick': price_tick, 'qty_step': qty_step}

    async def fetch_position(self):
        position_dict = await self.exchange.get_positions()
        self.position = position_dict.get(self.pair_symbol, None)

    async def fetch_order(self):
        self.orders = await self.exchange.get_order(self.pair_symbol)

    async def get_entry_signal(self):
        klines = await self.exchange.get_klines(pair_symbol=self.pair_symbol, interval=self.interval, limit=self.num_candles + 1)
        klines = klines.astype({'open': float, 'high': float, 'low': float, 'close': float})
        close = klines['close'].to_list()[-1]
        ma = klines['close'][:self.num_candles].mean()
        atr = ta.ATR(klines['high'], klines['low'], klines['close'], timeperiod=self.num_candles).to_list()[-1]
        entry_price = ma + atr * 3

        signal = Signal.ON if close > entry_price else Signal.OFF
        print(f'[TradingStrategy]-get_entry_signal: {close=}, {entry_price=}, signal={signal}')
        return signal

    def calc_tp_sl(self):
        pass

    def update_tp_sl(self):
        pass

    async def entry(self):
        entry_signal = await self.get_entry_signal()
        if entry_signal is Signal.OFF:
            print(f'[TradingStrategy]-entry: entry signal is OFF')
            return
        
        qty = 2
        await self.exchange.create_order(self.pair_symbol, qty, order_type='Market', side='Buy', price=None, reduce_only=False)
        print(f'[TradingStrategy]-entry: order is created')
        pass

    async def prepare(self):
        await self.fetch_position()
        await self.fetch_order()

    async def execute(self):
        print(f'[TradingStrategy]-execute: position={self.position}, orders={self.orders}')
        if self.position is None:
            await self.entry()

        self.update_tp_sl()
        pass


