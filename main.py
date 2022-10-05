from pynput.keyboard import Key, Controller
import pyperclip
import time

keyboard = Controller()
network_names = []
string = []
wifi_password = []


def copy_all():
    time.sleep(1)
    keyboard.press(Key.ctrl)
    keyboard.press('a')
    keyboard.release(Key.ctrl)
    keyboard.release('a')

    keyboard.press(Key.ctrl)
    keyboard.press('c')
    keyboard.release(Key.ctrl)
    keyboard.release('c')
    time.sleep(1)


def clear_cmd():
    time.sleep(0.5)
    keyboard.type("cls")
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)


#paste command to cmd
keyboard.press(Key.cmd_l)
keyboard.release(Key.cmd_l)
time.sleep(0.1)
keyboard.type("cmd")
time.sleep(0.1)
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(1)
keyboard.type("netsh wlan show profile")
keyboard.press(Key.enter)
keyboard.release(Key.enter)
time.sleep(1)

# copy to and paste from clipboard
copy_all()
words = pyperclip.paste()

# retrieve network name from cmd
names = words.split("All User Profile     : ")
for i in range(len(names)):
    if i == 0:
        continue
    network_names.append(names[i])

for i in range(len(network_names)):
    e = network_names[i].split("\r")
    if network_names[i] == network_names[-1]:
        e = network_names[i].split("\r\n\r\n\r\n")
    string += e


# lookup each wifi name and retrieve passwords
wifi_name = string[::2]
for i in range(len(wifi_name)):
    text = f'netsh wlan show profile name="{wifi_name[i]}" key=clear'
    keyboard.type(text)
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)

    copy_all()
    words = pyperclip.paste()
    if "Key Content" not in words:
        wifi_password.append("None")
        clear_cmd()
        continue
    names = words.split("Key Content            : ")
    password = names[1].split("\r\n\r\n")
    wifi_password.append(password[0])
    clear_cmd()

#exit the cmd
time.sleep(0.1)
keyboard.type("exit")
keyboard.press(Key.enter)
keyboard.release(Key.enter)

# create txt file to store passwords
f = open("passwords.txt", "w")
for i in range(len(wifi_name)):
    f.write(f'Wifi name: "{wifi_name[i]}" | Password: "{wifi_password[i]}"\n')
f.close()
