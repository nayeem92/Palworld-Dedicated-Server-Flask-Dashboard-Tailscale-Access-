# Palworld Dedicated Server + Flask Dashboard (Tailscale Access)

## Overview
This project allows you to self-host a **Palworld dedicated server** on a local Ubuntu machine, along with a **Flask-based web dashboard** accessible via Tailscale. It provides controls for starting, stopping, and restarting the game server, as well as editing key gameplay settings and creating backups of save data.

![alt text](/screenshots/image.png)
---

## Features
- Host your own Palworld server (v0.5.3)
- Start/Stop/Restart server from a web dashboard
- Change server settings like EXP rate, difficulty, stamina drain, etc.
- Backup game saves with one click
- Access the server dashboard from anywhere via Tailscale

![alt text](/screenshots/image-2.png)

---

## Requirements
- Ubuntu Server (tested on Ubuntu 24.04.2 LTS)
- SteamCMD (for downloading the game server)
- Python 3.10+
- Flask
- Tailscale (for secure remote access)

---

## Setup Guide

### 1. Install Dependencies
```bash
sudo apt update && sudo apt install python3-pip screen curl wget unzip -y
```

### 2. Manually Install SteamCMD
```bash
mkdir -p ~/tools/steamcmd && cd ~/tools/steamcmd
wget https://steamcdn-a.akamaihd.net/client/installer/steamcmd_linux.tar.gz
sudo apt install lib32gcc-s1 lib32stdc++6 -y
 tar -xvzf steamcmd_linux.tar.gz
```

### 3. Download Palworld Server
```bash
./steamcmd.sh +@sSteamCmdForcePlatformType windows +login anonymous +force_install_dir ~/palworld_053/server +app_update 2394010 validate +quit
```

### 4. Set Permissions and Run the Server
```bash
cd ~/palworld_053/server
chmod +x PalServer.sh
screen -S palworld ./PalServer.sh
```
(Use Ctrl+A, then D to detach)

---

## Flask Dashboard Setup

![alt text](/screenshots/image-1.png)

### 1. Clone the Dashboard
```bash
mkdir ~/palworld_dashboard_tailscale && cd ~/palworld_dashboard_tailscale
# Copy app.py and templates/index.html from this repo into this folder
```

### 2. Install Flask in a venv (Recommended)
```bash
python3 -m venv venv
source venv/bin/activate
pip install flask
```

### 3. Run Flask Dashboard
```bash
python3 app.py
```
Access it from: `http://<your-ip>:5000`

---

## Systemd Services (Optional)
To run automatically after reboot:

### Create systemd files:
```bash
sudo nano /etc/systemd/system/palworld.service
```
```ini
[Unit]
Description=Palworld Dedicated Server
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/screen -dmS palworld bash -c 'cd /home/<user-name>/palworld_053/server && ./PalServer.sh'
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
sudo nano /etc/systemd/system/paldashboard.service
```
```ini
[Unit]
Description=Palworld Flask Dashboard
After=network.target

[Service]
Type=simple
WorkingDirectory=/home/<user-name>/palworld_dashboard_tailscale
ExecStart=/usr/bin/python3 app.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable & start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable palworld.service paldashboard.service
sudo systemctl start palworld.service paldashboard.service
```

---

![alt text](/screenshots/image-4.png)
---
![alt text](/screenshots/image-3.png)

---

## Tailscale Setup (Brief)
Install Tailscale on your server and your devices, authenticate, and grab the Tailscale IP.

Once connected, access the dashboard from any authorized device:
```
http://<tailscale-ip>:5000
```

Use the same IP + port 8211 to join Palworld.

---

## Future Ideas
- Dockerize the entire stack
- Add user authentication to dashboard
- Show live player info via log/API polling

---

Made by Abdun Nayeem for personal gaming and self-hosting fun!

---
