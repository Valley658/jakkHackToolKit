import os
import pyfiglet
from colorama import Fore, Style, init

init(autoreset=True)

banner_text = """

      ██╗ █████╗ ██╗  ██╗██╗  ██╗
      ██║██╔══██╗██║ ██╔╝██║ ██╔╝
      ██║███████║█████╔╝ █████╔╝ 
 ██   ██║██╔══██║██╔═██╗ ██╔═██╗ 
 ╚█████╔╝██║  ██║██║  ██╗██║  ██╗
  ╚════╝ ╚═╝  ╚═╝╚═╝  ╚═╝╚═╝  ╚═╝

Jaxk Hacking Tool Kit Ver 2.1

Author : Jaxk
Contact : Not Support

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