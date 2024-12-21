from tools import *
from utils import *
from colorama import Fore, Style, init
import time

hacker_text = """

 ▄▀▀▄ ▄▄   ▄▀▀█▄   ▄▀▄▄▄▄   ▄▀▀▄ █  ▄▀▀█▄▄▄▄  ▄▀▀▄▀▀▀▄ 
█  █   ▄▀ ▐ ▄▀ ▀▄ █ █    ▌ █  █ ▄▀ ▐  ▄▀   ▐ █   █   █ 
▐  █▄▄▄█    █▄▄▄█ ▐ █      ▐  █▀▄    █▄▄▄▄▄  ▐  █▀▀█▀  
   █   █   ▄▀   █   █        █   █   █    ▌   ▄▀    █  
  ▄▀  ▄▀  █   ▄▀   ▄▀▄▄▄▄▀ ▄▀   █   ▄▀▄▄▄▄   █     █   
 █   █    ▐   ▐   █     ▐  █    ▐   █    ▐   ▐     ▐   
 ▐   ▐            ▐        ▐        ▐                  

"""

def printHacker():
    colors = [
        Fore.RED, Fore.YELLOW, Fore.GREEN, Fore.CYAN, Fore.BLUE, Fore.MAGENTA
    ]
    lines = hacker_text.splitlines()

    for i, line in enumerate(lines):
        color = colors[i % len(colors)]
        print(f"{color}{line}{Style.RESET_ALL}")

class Manager:
    def __init__(self):
        self.toolmanager = toolManager.toolManager()

    def run(self):
        while True:
            banner.printBanner()
            self.showMenu()
            print()
            cmd = input("> ")

            if cmd == "1":
                self.toolmanager.run()
            elif cmd == "2":
                jakkShellWin.main()
            elif cmd == "3":
                jakkShellLinux.main()
            elif cmd == "4":
                print("[-] Good Bye!")
                printHacker()
                time.sleep(1)
                exit()

            else:
                print("[*] Not Acceptable : {}".format(cmd))
    
    def showMenu(self):
        print("[ - Menu - ]")
        print("[1] Tools : {} Available".format(self.toolmanager.getNumToolList()))
        print("[2] Shell(Only Windows)")
        print("[3] Shell(Only Linux (e.g. ubuntu,Kali,CentOS))")
        print("[4] Exit")