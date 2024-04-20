#!/usr/local/bin/python3

import os
import asyncio
import pybotters
from dotenv import load_dotenv
from utils import get_current_time

from kairi_bot import ATRKairiBot


load_dotenv('/work/.env')

apis = {
    'bybit': [os.getenv('API_KEY'), os.getenv('API_SECRET')]
}

strategy_params = {
    'pair_symbol': os.getenv('pair_symbol'),
    'trading_volume': os.getenv('trading_volume'),
    'leverage': os.getenv('leverage'),
    'interval': os.getenv('interval'),
    'num_candles': os.getenv('num_candles')
}

async def main():
    async with pybotters.Client(apis=apis, base_url='https://api.bybit.com') as client:
        print('strategy_params:', strategy_params, '\n')
        kairi_bot = ATRKairiBot(client, strategy_params)
        await kairi_bot.run()

print(f'==================================  {get_current_time()}  ==================================')
asyncio.run(main())
print('\n')