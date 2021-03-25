from bs4 import BeautifulSoup
import requests 
from selenium import webdriver
import time
import os

class Fetch_id :

	def fetch(self,id_vid):

		chrome_options = webdriver.ChromeOptions()

		chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
		chrome_options.add_argument["--headless"]
		chrome_options.add_argument["--disable-dev-shm-usage"]
		chrome_options.add_argument["--no-sandbox"]
		driver = webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVE PATH'), chrome_options=chrome_optionse)

		url = f"https://ytdlink.herokuapp.com/{id_vid}"

		# PATH = "C:\Program Files (x86)\chromedriver.exe"

		# driver = webdriver.Chrome(PATH)

		driver.get(url)  

		time.sleep(10)

		soup = BeautifulSoup(driver.page_source,"html.parser")
		print(soup)
		return soup.body.div.string
