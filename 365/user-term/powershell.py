import subprocess

class PowerShell:
    def __init__(self):
        self.ps_process = subprocess.Popen(['powershell', '-NoExit', '-Command', '-'], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def send_command(self, command):
        self.ps_process.stdin.write(command + '\n')
        self.ps_process.stdin.flush()
        output = []
        while True:
            line = self.ps_process.stdout.readline()
            if line.strip() == "":
                break
            output.append(line.strip())
        return "\n".join(output)

def main():
    ps = PowerShell()
    print(ps.send_command("Connect-ExchangeOnline"))

main()