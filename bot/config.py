import json
import sys

from solana.rpc.api import Client
from solders.keypair import Keypair

from bot.log import logger


class Config(object):
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load_config()
            cls._instance.validate_config()
        return cls._instance

    def load_config(self):
        try:
            with open('config.json', 'r') as file:
                config_data = json.load(file)
                self.PRIVATE_KEY = config_data.get('PRIVATE_KEY')
                self.DISCORD_WEBHOOK = config_data.get('DISCORD_WEBHOOK')
                self.SLIPPAGE = config_data.get('SLIPPAGE')
                self.TOKEN_ADDRESS = config_data.get('TOKEN_ADDRESS')
                self.AMOUNT = config_data.get("AMOUNT")
                self.RPC = config_data.get('RPC') or 'https://api.mainnet-beta.solana.com'
        except Exception as e:
            logger.error(f"Error loading config.json: {e}")
            sys.exit(1)

    def validate_config(self):
        required_fields = ['PRIVATE_KEY', 'DISCORD_WEBHOOK', 'SLIPPAGE', 'TOKEN_ADDRESS', 'AMOUNT']
        missing_fields = [field for field in required_fields if not getattr(self, field, None)]

        if missing_fields:
            logger.error(f"Required config fields missing: {', '.join(missing_fields)}")
            sys.exit(1)

    @property
    def private_key(self):
        return Keypair.from_base58_string(self.PRIVATE_KEY)

    @property
    def public_key(self):
        return str(self.private_key.pubkey())

    @property
    def client(self):
        return Client(self.RPC)
