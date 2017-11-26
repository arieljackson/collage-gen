from django.shortcuts import render

# views.py
def get_screenshot(request):
    width = 1024
    height = 768

    if request.method == 'POST' and 'url' in request.POST:
        url = request.POST.get('url', '')
    driver = webdriver.Chrome(DRIVER)
    driver.get('https://www.wikipedia.com')
    driver.set_window_size(width, height)
    now = str(datetime.today().timestamp())
    img_dir = settings.MEDIA_ROOT
    img_name = ''.join([now, '_image.png'])
    full_img_path = os.path.join(img_dir, img_name)
    if not os.path.exists(img_dir):
        os.makedirs(img_dir)
    driver.save_screenshot(full_img_path)
    screenshot = open(full_img_path, 'rb').read()
    var_dict = {'screenshot': img_name, 'save': True}
    links = driver.find_elements_by_tag_name('a') 
    for link in links:
        driver.click(link)
    driver.quit()
