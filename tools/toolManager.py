from tools.addTool import *
from utils import *
import sys

class toolManager:
    def __init__(self):
        self.toolList = self.getToolList()

    def run(self):
        while True:
            banner.printBanner()
            self.showMenu()

            print()

            try:
                cmd = int(input("> "))
            except:
                print("[*] Not Acceptable : {}".format(cmd))
                continue

            if(cmd > self.getNumToolList()):
                print("[*] Tool exit...")
                return
            
            exeFunc = "{}.main()".format(self.toolList[cmd-1])
            eval(exeFunc)

    def getToolList(self):
        toolList = []
        for item in sys.modules.keys():
            if item.startswith("tools.addTool."):
                toolList.append(item[14:])
    
        return toolList
    
    def getNumToolList(self):
        return len(self.toolList)
    
    def showMenu(self):
        print("[ - Tool Menu - ]")

        idx = 1

        for tool in self.toolList:
            print("[{}] {}".format(idx, tool))
            idx += 1
            
        print("[{}] Exit".format(idx))