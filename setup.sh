#!/data/data/com.termux/files/usr/bin/bash
pkg update -y && pkg upgrade -y
pkg install -y python git
pip install -r requirements.txt
echo "NEONCRIPTO instalado. Execute: python app/neoncripto_cli.py"
