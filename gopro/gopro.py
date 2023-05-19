import subprocess
import sys
import os 
data = subprocess.run([sys.executable, "./gopro-ble-py/main.py --get-addresses-only"])

print(data)
