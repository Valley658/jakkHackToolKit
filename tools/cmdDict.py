class CommandDictionary:
    def __init__(self):
        self.commands = {
            # Linux Commands
            "ls": "dir",
            "pwd": "cd",
            "ifconfig": "ipconfig",
            "cat": "type",
            "touch": "echo. >",
            "mkdir": "mkdir",
            "rm": "del",
            "rmdir": "rmdir",
            "cp": "copy",
            "mv": "move",
            "sudo": "runas",
            "chmod": "attrib",
            "chown": "takeown",
            "df": "fsutil volume diskfree",
            "du": "dir /s",
            "find": "findstr",
            "grep": "findstr",
            "ps": "tasklist",
            "kill": "taskkill",
            "whoami": "whoami",
            "hostname": "hostname",
            "clear": "cls",

            # Windows Commands
            "dir": "dir",
            "cd": "cd",
            "cls": "cls",
            "type": "type",
            "ipconfig": "ipconfig",
            "runas": "runas",
            "echo": "echo",
            "pause": "pause",
            "shutdown": "shutdown",
            "tasklist": "tasklist",
            "taskkill": "taskkill",
            "tracert": "tracert",
            "netstat": "netstat",
            "nslookup": "nslookup",

            # Cross-platform Utilities
            "curl": "curl",
            "wget": "wget",
            "ping": "ping",
            "scp": "copy",
            "vim": "notepad",
            "nano": "notepad",
            "service": "net start",
            "systemctl": "net start",
            "mount": "subst",
            "unmount": "subst /d",

            # File System Operations
            "mkfile": "echo. >",
            "touch": "type nul >",
            "move": "move",
            "rename": "ren",
            "del": "del",
            "copy": "copy",

            # System Information
            "uname": "systeminfo",
            "uptime": "net statistics workstation",
            "free": "systeminfo | findstr /C:\"Available Physical Memory\"",
            "diskpart": "diskpart",
            "vol": "vol",

            # Networking Tools
            "arp": "arp",
            "route": "route",
            "dig": "nslookup",
            "ftp": "ftp",
            "ssh": "putty",  # Approximated as 'putty' for Windows
            "scp": "pscp",  # Secure copy using PuTTY tools

            # Development Tools
            "python": "python",
            "pip": "pip",
            "java": "java",
            "javac": "javac",
            "gcc": "gcc",
            "g++": "g++",
            "make": "nmake",

            # Monitoring Tools
            "top": "tasklist",
            "htop": "tasklist",
            "iotop": "typeperf",  # Approximation for disk IO stats
            "free": "typeperf",  # Approximation for memory usage stats

            # Disk and Storage
            "mount": "diskpart",
            "unmount": "diskpart",
            "lsblk": "wmic logicaldisk get size,freespace,caption",
            "blkid": "diskpart",
            "mkfs": "format",  # Filesystem creation
            "fsck": "chkdsk",  # Filesystem check
        }

    def get_commands(self):
        return self.commands

    def is_valid_command(self, command):
        base_command = command.split()[0]
        return base_command in self.commands

if __name__ == "__main__":
    cmd_dict = CommandDictionary()
    print("Available Commands:")
    for key, value in cmd_dict.get_commands().items():
        print(f"{key} -> {value}")