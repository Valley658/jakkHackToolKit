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

            # Cross-platform Utilities
            "help": "help",
            "whoami": "whoami",
            "hostname": "hostname",
            "date": "date /t",
            "time": "time /t",
            "clear": "cls",

            # Additional Commands
            "find": "findstr",  # Search for text within files (Windows equivalent)
            "grep": "findstr",  # Unix-like 'grep'
            "ps": "tasklist",  # List processes (Linux 'ps' equivalent)
            "kill": "taskkill",  # Kill process by name or ID
            "ping": "ping",  # Ping a network host
            "curl": "curl",  # Make HTTP requests
            "wget": "wget",  # Download files
            "netstat": "netstat",  # Display network connections
            "tracert": "tracert",  # Trace route to host
            "nslookup": "nslookup",  # Query DNS records
            "ftp": "ftp",  # File transfer protocol
            "scp": "copy",  # Secure copy (approximated for Windows)
            "vim": "notepad",  # Text editor (Linux 'vim' equivalent)
            "nano": "notepad",  # Text editor (Linux 'nano' equivalent)
            "service": "net start",  # Manage services (Windows equivalent of Linux 'service')
            "systemctl": "net start",  # System management commands
            "df": "fsutil volume diskfree",  # Disk space usage
            "du": "dir /s",  # Disk usage per directory
            "mount": "subst",  # Mount file systems
            "unmount": "subst /d",  # Unmount file systems
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