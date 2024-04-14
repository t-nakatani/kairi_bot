from exchange import Exchange
from strategy import Strategy

class ATRKairiBot:
    def __init__(self, client, config):
        exchange = Exchange(client)
        self.strategy = Strategy(exchange, config)
        self.config = config

    async def run(self):
        await self.strategy.initalize_setting()
        await self.strategy.prepare()
        await self.strategy.entry()
        pass

    
