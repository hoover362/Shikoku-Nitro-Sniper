import re
import os
import discord
import platform
import datetime
import requests

from colorama import Fore, init


class Sniper(discord.Client):
    """Our discord.py client"""

    def __init__(self, **options):
        super().__init__(**options)
        self.token = ""

    def client_headers(self):
        """Simply the headers needed to perform the requests"""
        return {
            'Authorization': self.token,
            'Content-Type': 'application/json',
        }

    @staticmethod
    def clear_console():
        if platform.system() != 'Linux':
            os.system('cls')
        else:
            os.system('clear')

    @staticmethod
    def replace_multiple(text):
        to_be_replaced = ['b', 'd', 'Y', '.', '`', "'", '~', 'V', 'o', 'D', 'P']
        for elem in to_be_replaced:
            if elem in text:
                text = text.replace(elem, f'{Fore.MAGENTA}{elem}{Fore.RESET}')
        return text

    def start_menu(self):
        banner = self.replace_multiple("""
            .d8888b.  888       d8b 888               888               
            d88P  Y88b 888      Y8P 888               888               
            Y88b.      888          888               888               
             "Y888b.   88888b.  888 888  888  .d88b.  888  888 888  888 
                "Y88b. 888 "88b 888 888 .88P d88""88b 888 .88P 888  888 
                  "888 888  888 888 888888K  888  888 888888K  888  888 
            Y88b  d88P 888  888 888 888 "88b Y88..88P 888 "88b Y88b 888 
             "Y8888P"  888  888 888 888  888  "Y88P"  888  888  "Y88888 
        """)
        print(banner + f"\n\n\t{Fore.MAGENTA}{datetime.datetime.now().strftime('%H:%M:%S %p')}{Fore.RESET} [1] Start nitro sniper")

        print(f"\n\t{Fore.MAGENTA}Enter your option{Fore.RESET}", end='')
        try:
            choice = int(input("  :  "))

            if choice == 1:
                self.clear_console()
                self.execute()

            else:
                self.clear_console()
                self.start_menu()

        except ValueError:
            self.clear_console()
            self.start_menu()

    async def on_connect(self):
        print(f"{Fore.MAGENTA}{datetime.datetime.now().strftime('%H:%M:%S %p')}{Fore.RESET} ({Fore.MAGENTA}CONNECTED{Fore.RESET}) => Logged in as {self.user.name} | {self.user.id}")

    async def claim_code(self, code: str):
        """Basic shortcut function to claim a gift code and return data"""
        r = requests.post(f'https://discordapp.com/api/v6/entitlements/gift-codes/{code}/redeem',
                          headers=self.client_headers(),
                          json={'channel_id': None, 'payment_source_id': None})
        if 'subscription_plan' not in r.text:
            try:
                message = r.json()['message']
            except (AttributeError, IndexError, KeyError):
                message = "cloudflare"
            return {'valid': False, 'message': message}
        else:
            return {'valid': True, 'message': r.json()}
              
    async def on_message(self, message):
        try:
            code = re.search(r'(discord.com/gifts/|discordapp.com/gifts/|discord.gift/)([a-zA-Z0-9]+)',
                             message.content)
            nitro_code = code.group(2)
            if code:
                if len(nitro_code) == 16 or len(nitro_code) == 24:
                    data = await self.claim_code(nitro_code)
                    data_message = data['message']
                    if 'subscription_plan' in data_message:
                        print(f"{Fore.MAGENTA}{datetime.datetime.now().strftime('%H:%M:%S %p')}{Fore.RESET} ({Fore.GREEN}Nitro Claimed{Fore.RESET}) - ({Fore.CYAN}{message.guild}{Fore.RESET}) - ({Fore.CYAN}{message.author.name}#{message.author.discriminator}{Fore.RESET}) - ({nitro_code})")
                    else:
                        print(f"{Fore.MAGENTA}{datetime.datetime.now().strftime('%H:%M:%S %p')}{Fore.RESET} ({Fore.RED}Nitro {data_message}{Fore.RESET}) - ({Fore.CYAN}{message.guild}{Fore.RESET}) - ({Fore.CYAN}{message.author.name}#{message.author.discriminator}{Fore.RESET}) - ({nitro_code})")

        except AttributeError:
            pass

    @staticmethod
    def check_if_connection_exists():
        """Checks if a internet connection exists (needed to run discord.py)"""
        try:
            requests.get('https://google.com/')
            return True
        except:
            return False

    def execute(self):
        """Executes the bot"""
        try:
            if self.check_if_connection_exists():
                super().run(self.token, bot=False)
            else:
                print(f"{Fore.MAGENTA}{datetime.datetime.now().strftime('%H:%M:%S %p')}{Fore.RESET} - (CONNECTION_ERR)")
                input("\n\n\nPress any key to exit...\n")
        except discord.errors.LoginFailure as e:
            print(f"{Fore.MAGENTA}{datetime.datetime.now().strftime('%H:%M:%S %p')}{Fore.RESET} - ({Fore.RED}{e}{Fore.RESET})")
            input("\n\n\nPress any key to exit...\n")


if __name__ == '__main__':
    if platform.system() != 'Linux':
        init(convert=True)
    client = Sniper()
    client.start_menu()
