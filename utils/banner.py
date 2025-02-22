import os
import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True)

banner_text = """
          _____                    _____                    _____                    _____          
         /\    \                  /\    \                  /\    \                  /\    \         
        /::\    \                /::\    \                /::\____\                /::\____\        
        \:::\    \              /::::\    \              /:::/    /               /:::/    /        
         \:::\    \            /::::::\    \            /:::/    /               /:::/    /         
          \:::\    \          /:::/\:::\    \          /:::/    /               /:::/    /          
           \:::\    \        /:::/__\:::\    \        /:::/____/               /:::/____/           
           /::::\    \      /::::\   \:::\    \      /::::\    \              /::::\    \           
  _____   /::::::\    \    /::::::\   \:::\    \    /::::::\____\________    /::::::\____\________  
 /\    \ /:::/\:::\    \  /:::/\:::\   \:::\    \  /:::/\:::::::::::\    \  /:::/\:::::::::::\    \ 
/::\    /:::/  \:::\____\/:::/  \:::\   \:::\____\/:::/  |:::::::::::\____\/:::/  |:::::::::::\____\\
\:::\  /:::/    \::/    /\::/    \:::\  /:::/    /\::/   |::|~~~|~~~~~     \::/   |::|~~~|~~~~~     
 \:::\/:::/    / \/____/  \/____/ \:::\/:::/    /  \/____|::|   |           \/____|::|   |          
  \::::::/    /                    \::::::/    /         |::|   |                 |::|   |          
   \::::/    /                      \::::/    /          |::|   |                 |::|   |          
    \::/    /                       /:::/    /           |::|   |                 |::|   |          
     \/____/                       /:::/    /            |::|   |                 |::|   |          
                                  /:::/    /             |::|   |                 |::|   |          
                                 /:::/    /              \::|   |                 \::|   |          
                                 \::/    /                \:|   |                  \:|   |          
                                  \/____/                  \|___|                   \|___|          

Jakk Hacking Tool Kit Ver 5.0

Author : Null
Contact : Discord 1hgi3b (Null)

"""

def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):
        command = 'cls'
    os.system(command)

def printBanner():
    clearConsole()
    colors = [
        Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA
    ]
    lines = banner_text.splitlines()

    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(f"{color}{line}{Style.RESET_ALL}")

if __name__ == "__main__":
    printBanner()
