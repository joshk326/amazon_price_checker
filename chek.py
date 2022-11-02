import requests
import time
import traceback
import sys
import os

try:
	from bs4 import BeautifulSoup
	import lxml
	import sys
except ImportError:
	import subprocess

	def checkRequirements():
		"""Check if the user has the required dependencies, if not, ask to install them"""
		if os.name == 'nt': # Windows
			import ctypes
			MessageBox = ctypes.windll.user32.MessageBoxW
			result = MessageBox(None, "Missing required modules, do you want to install these?\nThis will take a minute", "Missing bs4/lxml", 4)
		else: # Assume POSIX
			print("Install missing bs4/lxml libraries? [(Y)es/No]")
			if input().lower() in {'yes','ye', 'y', ''}:
				result = 6 # Same as MessageBoxW yes on Win32
			else:
				result = 7 # Same as MessageBoxW no on Win32, but it could really be anything

		if result == 6: # User agreed to installation
			print("Please wait a moment while modules are being installed")
			# https://pip.pypa.io/en/latest/user_guide/#using-pip-from-your-program
			subprocess.check_call([sys.executable, "-m", "pip", "install", "bs4"])
			subprocess.check_call([sys.executable, "-m", "pip", "install", "lxml"])
			print("Done")
			print("-------------")
			subprocess.check_call([sys.executable, sys.argv[0]])
		sys.exit()

	checkRequirements()

class bcolors:
    HEADER = '\033[95m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    RED = '\033[91m'
    DEFAULT = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def runner(delay, func, args):
	next_time = time.time() + delay
	while True:
		time.sleep(max(0, next_time - time.time()))
		try:
			func(args)
		except Exception:
			traceback.print_exc()
		
		next_time += (time.time() - next_time)

def get_price(url):
	headers = {
	"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
				"(KHTML, like Gecko) Chrome/98.0.4758.82 Safari/537.36",
	"Accept-Language": "en-US,en;q=0.9"
	}

	response = requests.get(url = url, headers=headers)

	results = response.text
	cleaned = BeautifulSoup(results, "lxml")
	currency = cleaned.find(name="span", class_="a-price-symbol").getText()
	dollar = cleaned.find(name="span", class_="a-price-whole").getText()
	decimal = cleaned.find(name="span", class_="a-price-fraction").getText()
	price = currency + dollar + decimal
	print(time.time(), "\n")
	print(bcolors.DEFAULT + bcolors.BOLD + bcolors.GREEN +"Price:", price + bcolors.DEFAULT+"\n")

if len(sys.argv) == 3:
	print(bcolors.UNDERLINE + bcolors.BOLD + bcolors.CYAN + "Use CTRL + C to end the program")
	runner(int(sys.argv[1]), get_price, str(sys.argv[2]))
else:
	print(bcolors.RED + "<USAGE> python check.py \"<time-interval (in seconds)>\" \"<url>\"")