import requests
from tabulate import tabulate

from bot.config import Config


class Wallet(Config):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def fetch_tokens(self):
        account_info = requests.post(
            self.RPC,
            json={
                "jsonrpc": "2.0",
                "id": 1,
                "method": "getTokenAccountsByOwner",
                "params": [
                    self.public_key,
                    {"programId": "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"},
                    {"encoding": "jsonParsed"}
                ]
            }
        )

        if account_info.ok:
            account_data_json = account_info.json()
            accounts = account_data_json.get('result', {}).get('value', [])
            fetched_data = {account['account']['data']['parsed']['info']['mint']:
                                account['account']['data']['parsed']['info']['tokenAmount']['uiAmount']
                            for account in accounts}
            return fetched_data
        else:
            return None

    def get_token_price(self, mint_addresses):
        addresses = ','.join(mint_addresses)
        req = requests.get(
            f"https://api.dexscreener.com/latest/dex/tokens/{addresses}"
        )

        if req.ok:
            fetched_data = {}
            data = req.json()
            for pair in data['pairs']:
                base_token = pair['baseToken']
                quote_token = pair['quoteToken']
                price_native = pair['priceNative']
                price_usd = pair['priceUsd']

                if quote_token['symbol'] == 'SOL':
                    mint_address = base_token['address']
                    if mint_address not in fetched_data:
                        fetched_data[mint_address] = {
                            'base_token_symbol': base_token['symbol'],
                            'quote_token_symbol': quote_token['symbol'],
                            'price_native': price_native,
                            'price_usd': price_usd
                        }

            return fetched_data
        else:
            return None

    def print_token_prices(self, token_prices, tokens_with_amounts):
        table_data = []
        for mint, details in token_prices.items():
            amount = tokens_with_amounts.get(mint, 'N/A')
            price_native = float(details['price_native'])
            price_usd = float(details['price_usd'])

            if amount != 'N/A':
                value_sol = amount * price_native
                value_usd = amount * price_usd
            else:
                value_sol = value_usd = 'N/A'

            table_data.append([
                mint,
                f"{details['base_token_symbol']}/{details['quote_token_symbol']}",
                amount,
                price_native,
                price_usd,
                value_sol,
                value_usd
            ])
        headers = ["Mint Address", "Pair", "Amount", "Unit Price (SOL)", "Unit Price (USD)", "Value (SOL)",
                   "Value (USD)"]
        print(tabulate(table_data, headers, tablefmt="rounded_grid", numalign="center"))

    def start(self):
        tokens_with_amounts = self.fetch_tokens()
        if tokens_with_amounts:
            token_addresses = list(tokens_with_amounts.keys())
            token_prices = self.get_token_price(token_addresses)
            self.print_token_prices(token_prices, tokens_with_amounts)
        else:
            print("No tokens found...")
