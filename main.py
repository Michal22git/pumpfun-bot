from InquirerPy import inquirer
from pyfiglet import Figlet

from bot.config import Config
from bot.wallet import Wallet

class Menu(Config):

    def display_logo(self):
        print("\033c", end="")
        print(Figlet(font='slant').renderText('PumpFun Bot'))

    def menu(self):
        self.display_logo()
        choices = inquirer.select(
            message="Select option:",
            choices=[
                "PumpFun Sniper",
                "Wallet",
                "Configuration",
                "Exit"
            ]
        ).execute()

        if choices == "PumpFun Sniper":
            pass
        elif choices == "Wallet":
            Wallet().start()
            input("")
            return self.menu()
        elif choices == "Configuration":
            print("Private Key: ", self.PRIVATE_KEY)
            print("RPC: ", self.RPC)
            print("Token Address: ", self.TOKEN_ADDRESS)
            print("Amount (SOL):", self.AMOUNT)
            print("Slippage (%):", self.SLIPPAGE)
            print("Discord Webhook: ", self.DISCORD_WEBHOOK)

            input("")

            return self.menu()
        elif choices == "Exit":
            pass
        else:
            print("Invalid choice")
            return self.menu()


if __name__ == '__main__':
    obj = Menu()
    obj.menu()
