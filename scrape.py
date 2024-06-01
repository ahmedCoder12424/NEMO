from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.core.os_manager import ChromeType
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import random
import time
import sqlite3
#import easyocr

service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
opt = [
    "--headless=new",
    "--disable-gpu",
    "--ignore-certificate-errors",
    "window-size=1920,1200",
    "--disable-extensions",
    "--no-sandbox",
    "--disable-dev-shm-usage"]
#options.add_argument('--headless=new') #open browser in background
for o in opt:
    options.add_argument(o)
driver = webdriver.Chrome(service=service, options=options)
driver.get('https://www.instagram.com')

username = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='username']")))
password = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[name='password']")))
username.clear()
password.clear()
username.send_keys('folsomfatties69')
time.sleep(0.5)
password.send_keys('fattyPatties31$')

log_in = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()
time.sleep(5)
try:
    popup = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div[tabindex='0']"))).click()
    time.sleep(0.5)
    popup2 = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button[class='_a9-- _ap36 _a9_1']"))).click()
except:
    pass
driver.get('https://www.instagram.com/?variant=following')

time.sleep(2)
driver.execute_script("window.scrollBy(0, 400);")
time.sleep(2)
lastPost =  driver.find_elements(By.CSS_SELECTOR,"div[class='x78zum5 xdt5ytf x5yr21d xa1mljc xh8yej3 x1bs97v6 x1q0q8m5 xso031l x11aubdm xnc8uc2']")[-1]
lastPostID = lastPost.find_element(By.CSS_SELECTOR,"div[class='x1rg5ohu xw3qccf']").text + lastPost.find_element(By.CSS_SELECTOR,"span[class='_ap3a _aaco _aacu _aacx _aad7 _aade']").text[:10]
driver.get('https://www.instagram.com/?variant=following')
time.sleep(2)

postSet = set()
#reader = easyocr.Reader(['en'])
posts = []
usernames = []
imgs = []
captions = []
keys = []

keywords = ['free', 'chipotle', 'food', 'snack', 'boba', 'tea', 'sandwich', 'pizza', 'donut', 'bahn mi', 'cookie', 
           'cater', 'potluck', 'bake', 'weed', 'alchohol', 'pyschedel']

i = 0
while lastPostID not in postSet:
    temp = driver.find_element(By.CSS_SELECTOR,"div[class='x78zum5 xdt5ytf x5yr21d xa1mljc xh8yej3 x1bs97v6 x1q0q8m5 xso031l x11aubdm xnc8uc2']")
    #if posts and temp == posts[-1]:
    if temp.find_element(By.CSS_SELECTOR,"div[class='x1rg5ohu xw3qccf']").text + temp.find_element(By.CSS_SELECTOR,"span[class='_ap3a _aaco _aacu _aacx _aad7 _aade']").text[:10] in postSet:
        driver.execute_script("window.scrollBy(0, 400);")
    else:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "span[class='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm x1roi4f4 x1yc453h x10wh9bi x1wdrske x8viiok x18hxmgj']"))).click()
        posts.append(temp)

        while True:
            try:
                usernames.append(temp.find_element(By.CSS_SELECTOR,"div[class='x1rg5ohu xw3qccf']").text)
                break
            except Exception as e:
                driver.execute_script("window.scrollBy(0, -400);")
                time.sleep(1)
            
        postSet.add(temp.find_element(By.CSS_SELECTOR,"div[class='x1rg5ohu xw3qccf']").text + temp.find_element(By.CSS_SELECTOR,"span[class='_ap3a _aaco _aacu _aacx _aad7 _aade']").text[:10])
        keys.append(temp.find_element(By.CSS_SELECTOR,"div[class='x1rg5ohu xw3qccf']").text + temp.find_element(By.CSS_SELECTOR,"span[class='_ap3a _aaco _aacu _aacx _aad7 _aade']").text[:10])

        captions.append(temp.find_element(By.CSS_SELECTOR,"span[class='_ap3a _aaco _aacu _aacx _aad7 _aade']").text)
        
        try:
            image = temp.find_element(By.CSS_SELECTOR,"div[class='_aagv']>img")
            imgs.append(image.get_attribute('src'))
        except:
            captions.pop()
            keys.pop()
            usernames.pop()

    i += 1
    print('added post' + str(i))   
    time.sleep(1)

driver.quit()

con = sqlite3.connect("app/posts.db")
cur = con.cursor()
for i in range(len(keys)):
    row = (keys[i], usernames[i], captions[i], imgs[i])
    cur.execute("INSERT OR IGNORE INTO posts VALUES(?, ?, ?, ?)", row)
con.commit()
con.close()
