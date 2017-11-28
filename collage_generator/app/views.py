from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import base64
import os
import math
import urllib.parse as urlparse
from datetime import datetime
import time
from selenium.webdriver.chrome.options import Options
from PIL import Image
import math
import glob
import random

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
DRIVER = 'chromedriver'

# views.py
def get_screenshot(request):


    username = os.getenv("USERNAME")
    userProfile = "C:\\Users\\", username, "\\AppData\\Local\\Google\\Chrome\\User Data\\Default"
    _chrome_options = Options()
    _chrome_options.add_argument('disable-infobars')
    _chrome_options.add_argument("user-data-dir={}".format(userProfile))

    if request.method == 'POST' and 'url' in request.POST:
        url = request.POST.get('url', '')

        driver = webdriver.Chrome(DRIVER, chrome_options = _chrome_options)
        driver.get(url)


        now = str(datetime.today().timestamp())
        website = url.replace('/', '.')
        media_dir = settings.MEDIA_ROOT
        img_dir = ''.join([now, website])
        img_paths = []
        max_runs = 15 #todo make this param
        for i in range(max_runs):
            print("i is", i)
            # driver.manage().timeouts().implicitlyWait(20, TimeUnit.SECONDS);
            img_name = ''.join([str(i), '_image.png'])
            full_path = os.path.join(media_dir, img_dir)
            full_img_path = os.path.join(media_dir, img_dir, img_name)
            img_paths.append(full_img_path)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
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
                index = random.randint(0, index)
                if (index == num_links):
                    index = index-1
                print(index)
                attribute = links[index].get_attribute("href")
                print(attribute) 
                driver.get(attribute)
            except:
                break

        imagelist = [Image.open(path) for path in img_paths]
        width = 2880
        height = 1800
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

        collage_name = 'collage.png'
        rel_collage_path = os.path.join(img_dir, collage_name)
        full_collage_path = os.path.join(media_dir, img_dir, collage_name)
        all_collages = os.path.join(media_dir, collage_name)
        var_dict = {'collage': rel_collage_path}
        new_im.save(full_collage_path)
        new_im.save(all_collages)
        driver.quit()
        os.system('open ' + full_collage_path)
        print('here')
        return render(request, 'home.html', var_dict)
    else:
        return HttpResponse('Error')


