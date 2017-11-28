from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import base64
import os
import math
import urllib.parse as urlparse
from datetime import datetime
from selenium import webdriver
import time
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
import numpy as np
import pickle
import math
import glob
import matplotlib.pyplot as plt
import random

""" Save a screenshot from spotify.com in current directory"""
website = 'twitter.com/barackobama'
url = ('https://www.' + website)
DRIVER = 'chromedriver'
username = os.getenv("USERNAME")
userProfile = "C:\\Users\\", username, "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
_chrome_options = Options()
_chrome_options.add_argument('disable-infobars')
_chrome_options.add_argument("user-data-dir={}".format(userProfile))
driver = webdriver.Chrome(DRIVER, chrome_options = _chrome_options)
driver.get(url)

now = str(datetime.today().timestamp())
img_dir = ''.join([now, website])
img_paths = []
max_runs = 15
for i in range(max_runs):
	print("i is", i)
	# driver.manage().timeouts().implicitlyWait(20, TimeUnit.SECONDS);
	img_name = ''.join([str(i), '_image.png'])
	full_img_path = os.path.join(img_dir, img_name)
	img_paths.append(full_img_path)
	if not os.path.exists(img_dir):
	    os.makedirs(img_dir)
	driver.save_screenshot(full_img_path)
	screenshot = open(full_img_path, 'rb').read()
	var_dict = {'screenshot': img_name, 'save': True}
	# links = driver.find_elements_by_tag_name('a')
	try:
		links = driver.find_elements_by_xpath("//a[@href]")
		num_links = len(links)
		print(num_links)
		if num_links == 0:
			break
		index = math.floor((i / max_runs) * num_links)
		if (index == num_links):
			index = index-1
		print(index)
		attribute = links[index].get_attribute("href")
		print(attribute) 
		driver.get(attribute)
	except:
		break

imagelist = [Image.open(path) for path in img_paths]
width = 1200
height = 1000
new_im = Image.new('RGB', (width, height))
for i, image in enumerate(imagelist):
	if i == 0:
		denom = 2
	else:
		denom = max_runs + 1 - i
	resized_width = width // denom
	resized_height = height // denom
	x = random.randint(0, width - resized_width)
	y = random.randint(0, height - resized_height)
	resized = image.resize([resized_width,resized_height], Image.ANTIALIAS)
	new_im.paste(resized, (x, y))

new_im.save("Collage.jpg")
driver.quit()

