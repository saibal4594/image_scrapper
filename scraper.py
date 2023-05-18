import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Chrome







def fetch_image_urls(query: str, max_links_to_fetch: int, wd: webdriver, sleep_between_interactions: int = 1):
    def scroll_to_end(wd):
        wd.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(sleep_between_interactions)

        # build the google query

    search_url = "https://www.google.com/search?q={q}&rlz=1C1VDKB_enIN1013IN1013&sxsrf=APwXEdcU3RaClUsZmGGXheSy88drqps7EQ:1683869180931&source=lnms&tbm=isch&sa=X&ved=2ahUKEwi2jYLDhe_-AhX9R2wGHc4hBbQQ_AUoAXoECAEQAw&biw=1280&bih=569&dpr=1.5"

    # load the page
    wd.get(search_url.format(q=query))

    image_urls = set()
    image_count = 0
    results_start = 0
    while image_count < max_links_to_fetch:
        scroll_to_end(wd)

        # get all image thumbnail results
        thumbnail_results = wd.find_elements(By.CSS_SELECTOR,"img.Q4LuWd")

        for img in thumbnail_results:
            # Get the image URL
            image_url = img.get_attribute('src')

            # Add the image URL to the set of image URLs
            image_urls.add(image_url)
        print("check here 101")
        print(len(image_urls))
        image_urls = list(image_urls)
        print(image_urls)
        number_results = len(image_urls)
        print(image_urls[0])
        print(f"Found: {number_results} search results. Extracting links from {results_start}:{number_results}")
        #print(image_urls)
        print(type(image_urls))

        for i, img in enumerate(image_urls, start=1):
            # Try to click every thumbnail to get the real image behind it
            try:
                print(f"Clicking image {i}/{len(image_urls)}")
                img_element = wd.find_element(By.XPATH, f"//img[@src='{img}']")
                img_element.click()
                time.sleep(sleep_between_interactions)
            except Exception:
                continue

            # extract image urls
            actual_images = wd.find_elements(By.CSS_SELECTOR, 'img.n3VNCb')
            print("check")
            print(actual_images)
            for actual_image in actual_images:
                print("check actual_image")
                print(actual_image)
                if actual_image.get_attribute('src') and 'http' in actual_image.get_attribute('src'):
                    image_urls.add(actual_image.get_attribute('src'))
                    print(image_urls)
                    print("url found")
            image_urls_list = list(image_urls)

            #print(image_urls_list)
            image_count = len(image_urls_list)

            if len(image_urls) >= max_links_to_fetch:
                print(f"Found: {len(image_urls_list)} image links, done!")
                break
        else:
            print("Found:", len(image_urls_list), "image links, looking for more ...")
            time.sleep(30)
            # return
            load_more_button = wd.find_elements(By.CSS_SELECTOR,".mye4qd")
            if load_more_button:
                wd.execute_script("document.querySelector('.mye4qd').click();")

    # move the result startpoint further down
        results_start = len(thumbnail_results)

    return image_urls



def persist_image(folder_path:str,url:str, counter):
    #image_content = None
    try:
        image_content = requests.get(url).content

    except Exception as e:
        print(f"ERROR - Could not download {url} - {e}")

    try:
        f = open(os.path.join(folder_path, 'jpg' + "_" + str(counter) + ".jpg"), 'wb')
        f.write(image_content)
        f.close()
        print(f"SUCCESS - saved {url} - as {folder_path}")
    except Exception as e:
        print(f"ERROR - Could not save {url} - {e}")


def search_and_download(search_term: str, driver_path: str, target_path='./images', number_images=10):
    target_folder = os.path.join(target_path, '_'.join(search_term.lower().split(' ')))

    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    with webdriver.Chrome(executable_path=driver_path) as wd:
        res = fetch_image_urls(search_term, number_images, wd=wd, sleep_between_interactions=0.5)

    counter = 0
    for elem in res:
        persist_image(target_folder, elem, counter)
        counter += 1


# How to execute this code
# Step 1 : pip install selenium. pillow, requests
# Step 2 : make sure you have chrome installed on your machine
# Step 3 : Check your chrome version ( go to three dot then help then about google chrome )
# Step 4 : Download the same chrome driver from here  " https://chromedriver.storage.googleapis.com/index.html "
# Step 5 : put it inside the same folder of this code


DRIVER_PATH = r'C:\Users\mrcha\Downloads\ImageScrapper\ImageScrapper\chromedriver.exe'
search_term = 'AUDI'
# num of images you can pass it from here  by default it's 10 if you are not passing
#number_images = 50
search_and_download(search_term=search_term, driver_path=DRIVER_PATH, number_images=10)