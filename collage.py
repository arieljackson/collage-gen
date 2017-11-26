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

""" Save a screenshot from spotify.com in current directory"""
DRIVER = 'chromedriver'
username = os.getenv("USERNAME")
userProfile = "C:\\Users\\", username, "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
_chrome_options = Options()
_chrome_options.add_argument('disable-infobars')
_chrome_options.add_argument("user-data-dir={}".format(userProfile))
driver = webdriver.Chrome(DRIVER, chrome_options = _chrome_options)
driver.get('https://www.facebook.com')
# driver.set_winçow_size(width, height)

def wait_for(condition_function):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function():
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

def click_through_to_new_page(link, my_id):
    link.click()

    def link_has_gone_stale():
        try:
            # poll the link with an arbitrary call
            link.find_elements_by_id(my_id) 
            return False
        except StaleElementReferenceException:
            return True

    wait_for(link_has_gone_stale)


for i in range(15):
	print("i is", i)
	# driver.manage().timeouts().implicitlyWait(20, TimeUnit.SECONDS);
	now = str(datetime.today().timestamp())
	img_dir = 'testing'
	img_name = ''.join([now, '_image.png'])
	full_img_path = os.path.join(img_dir, img_name)
	if not os.path.exists(img_dir):
	    os.makedirs(img_dir)
	driver.save_screenshot(full_img_path)
	screenshot = open(full_img_path, 'rb').read()
	var_dict = {'screenshot': img_name, 'save': True}
	# links = driver.find_elements_by_tag_name('a')
	links = driver.find_elements_by_xpath("//a[@href]")
	num_links = len(links)
	print(num_links)
	index = math.floor((i / 15) * num_links)
	print(index)
	# attribute = links[3].get_attribute('id'); 
	attribute = links[index].get_attribute("href")
	print(attribute) 
	# driver.maximize_window()
	driver.get(attribute)
	# click_through_to_new_page(links[0], attribute)
	# timeout = 5
	# element_present = EC.presence_of_element_located((By.TAG, 'a'))
	# WebDriverWait(driver, timeout).until(element_present)
driver.quit()

