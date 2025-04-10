#!/bin/bash

# Enable camera and set up Arducam IMX708
echo "dtoverlay=imx708" | sudo tee -a /boot/config.txt
raspi-config nonint do_camera 0

# Update & install packages
sudo apt update
sudo apt install -y python3-pip libatlas-base-dev libopenjp2-7 libtiff5 libjpeg-dev libavcodec-dev libavformat-dev libswscale-dev libqtgui4 libqt4-test libilmbase-dev libopenexr-dev libgstreamer1.0-dev

# Python libraries
pip3 install face_recognition pyttsx3 SpeechRecognition gpiozero opencv-python RPi.GPIO numpy

# Set ReSpeaker mic as default
echo '
pcm.!default {
  type asym
  capture.pcm "mic"
}
pcm.mic {
  type plug
  slave {
    pcm "hw:1,0"
  }
}
' | sudo tee /etc/asound.conf

# Clone repo if not already there
if [ ! -d "/home/pi/Zarn" ]; then
  git clone https://github.com/CryptoTom/Zarn.git /home/pi/Zarn
fi

echo "ZARN setup complete. Rebooting now..."
sleep 3
sudo reboot
