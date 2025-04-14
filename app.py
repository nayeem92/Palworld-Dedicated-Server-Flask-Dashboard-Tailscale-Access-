from flask import Flask, render_template, request, redirect
import subprocess
import os
import re
from datetime import datetime

app = Flask(__name__)

INI_PATH = os.path.expanduser("~/palworld_053/server/Pal/Saved/Config/LinuxServer/PalWorldSettings.ini")
SAVE_PATH = os.path.expanduser("~/palworld_053/server/Pal/Saved/SaveGames/0")

def get_server_status():
    result = subprocess.run(["screen", "-ls"], capture_output=True, text=True)
    return "palworld" in result.stdout

def parse_ini():
    if not os.path.exists(INI_PATH):
        return {}

    with open(INI_PATH, "r") as f:
        content = f.read()

    match = re.search(r"OptionSettings=\((.*?)\)", content, re.DOTALL)
    if not match:
        return {}

    settings_str = match.group(1)
    settings = {}
    for item in settings_str.split(","):
        if "=" in item:
            key, value = item.strip().split("=", 1)
            settings[key.strip()] = value.strip().strip('"')

    return settings

def save_ini(new_settings):
    ini_data = "[/Script/Pal.PalGameWorldSettings]\n"
    option_string = ",".join([f'{k}={v}' for k, v in new_settings.items()])
    ini_data += f"OptionSettings=({option_string})\n"

    with open(INI_PATH, "w") as f:
        f.write(ini_data)

@app.route("/")
def index():
    status = get_server_status()
    settings = parse_ini()
    return render_template("index.html", status=status, settings=settings, ip="100.113.88.109")

@app.route("/start", methods=["POST"])
def start_server():
    subprocess.Popen("screen -dmS palworld bash -c 'cd ~/palworld_053/server && ./PalServer.sh'", shell=True)
    return redirect("/")

@app.route("/stop", methods=["POST"])
def stop_server():
    subprocess.run("screen -S palworld -X quit", shell=True)
    return redirect("/")

@app.route("/restart", methods=["POST"])
def restart_server():
    subprocess.run("screen -S palworld -X quit", shell=True)
    subprocess.Popen("screen -dmS palworld bash -c 'cd ~/palworld_053/server && ./PalServer.sh'", shell=True)
    return redirect("/")

@app.route("/save", methods=["POST"])
def save_settings():
    updated = {k: v for k, v in request.form.items()}
    save_ini(updated)
    return redirect("/")

@app.route("/backup_game", methods=["POST"])
def backup_game_save():
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_dir = os.path.expanduser(f"~/palworld_053/backups/saves/save_backup_{timestamp}")
    os.makedirs(backup_dir, exist_ok=True)

    # Copy the whole save folder
    subprocess.run(f"cp -r {SAVE_PATH}/* {backup_dir}/", shell=True)
    return redirect("/")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
