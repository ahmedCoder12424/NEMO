from flask import Flask, render_template
from selenium import webdriver
from selenium.webdriver.common.by import By

app = Flask(__name__)

@app.route("/")
def index():
    options = webdriver.ChromeOptions()
    options.add_argument("--headless=new")

    driver = webdriver.Chrome(options=options)
    driver.get('http://www.scrapethissite.com/pages/simple/')

    countries = driver.find_elements(By.CSS_SELECTOR, "div[class='col-md-4 country']")
    names = [c.find_element(By.CSS_SELECTOR, "h3[class='country-name']").text for c in countries]
    driver.quit()

    return render_template('index.html', names=names)