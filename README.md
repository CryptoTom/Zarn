# ZARN_1

This is the private repo for ZARN — a voice-controlled AI robot assistant running on a Raspberry Pi 4. Features include turret movement, camera, voice interface, and BB-firing module.

## Setup Instructions

1. **Clone this repo to your Raspberry Pi**
```bash
git clone https://github.com/CryptoTom/Zarn.git
cd Zarn
```

2. **Make setup script executable**
```bash
chmod +x setup_zarn.sh
```

3. **Run the setup**
```bash
./setup_zarn.sh
```

4. **(Optional) Auto-start ZARN on boot**
Create a file called `zarn.service`:
```
[Unit]
Description=ZARN AI Assistant
After=network.target

[Service]
ExecStart=/usr/bin/python3 /home/pi/Zarn/run_zarn.py
WorkingDirectory=/home/pi/Zarn
StandardOutput=inherit
StandardError=inherit
Restart=always
User=pi

[Install]
WantedBy=multi-user.target
```
Then enable it:
```bash
sudo cp zarn.service /etc/systemd/system/
sudo systemctl enable zarn.service
sudo systemctl start zarn.service
```

5. **Reboot and test**
```bash
sudo reboot
```

ZARN should auto-start. You can also run it manually:
```bash
python3 run_zarn.py
```
