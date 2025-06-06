#!/bin/bash

echo "Installing System Packages"
sudo apt-get update
sudo apt-get install -y python3-venv qt5-default libqt5gui5 libqt5test5

echo "Creating virtual environment"
python3 -m venv venv

echo "Activating virtual enviroment"
source venv/bin/activate

echo "Installing Python packages from requirements.txt"
pip install --upgrade pip
pip install -r requirements.txt

echo -e "✅ Install complete\n📸 Make sure you manually ENABLE the CAMERA PORT in raspi-config."

exit 0
