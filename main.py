import subprocess
Wifi_Names = []
Passwords = []

info = subprocess.run("netsh wlan show profile", capture_output=True).stdout.decode()
temp = info.split("    All User Profile     : ")

for name in temp:
    Wifi_Names.append(name.split("\r")[0])
if Wifi_Names[0] == '':
    Wifi_Names.pop(0)

for name in Wifi_Names:
    keyInfo = subprocess.run(["netsh", "wlan", "show", "profile", name, "key=clear"], capture_output=True).stdout.decode()
    try:
        names = keyInfo.split("Key Content            : ")
        temp = names[1].split("\r\n\r\n")
        Passwords.append(temp[0])
    except:
        Passwords.append("Open or Unavailable")

f = open(f"passwords({len(Passwords)}).txt", "w")
for i in range(len(Wifi_Names)):
    f.write(f'Wifi_Name: {Wifi_Names[i]}\nPassword: {Passwords[i]}\n\n')
f.close()
