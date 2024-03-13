from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import time, json

datas = []
options = FirefoxOptions()
options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
iterations = 0

def get_data(urls, driver, iterations):
    if iterations > 5:
        return
    iterations+=1
    urls = []
    print("Firefox Headless Browser Invoked")
    for url in urls:
        print("Getting data from: " + url)
        data = {
            "title": "",
            "year": 0,
            "rating": 0,
            "genres": [],
            "directors": [],
            "writers": [],
            "stars": []
        }

        driver.get(url)

        # Get the title, year, genres of the movie
        data["title"] = driver.find_element(By.CSS_SELECTOR, ".hero__primary-text").text
        data["year"] = int(driver.find_element(By.CSS_SELECTOR, "div.sc-69e49b85-0.jqlHBQ > ul > li:nth-child(1) > a").text)
        data["rating"] = float(driver.find_element(By.CSS_SELECTOR, "div.sc-3a4309f8-0.bjXIAP.sc-69e49b85-1.llNLpA > div > div:nth-child(1) > a > span > div > div.sc-bde20123-0.dLwiNw > div.sc-bde20123-2.cdQqzc > span.sc-bde20123-1.cMEQkK").text.replace(",", "."))

        # Get the  of the movie
        a = driver.find_elements(By.CSS_SELECTOR , "div.ipc-chip-list__scroller > a > span")
        for i in a:
            data["genres"].append(i.text)

        # Get the directors of the movie
        b = driver.find_elements(By.CSS_SELECTOR, "div.sc-69e49b85-3.dIOekc > div > ul > li:nth-child(1) > div > ul > li > a")
        for i in b:
            data["directors"].append(i.text)

        # Get the writers of the movie
        c = driver.find_elements(By.CSS_SELECTOR, "div.sc-69e49b85-3.dIOekc > div > ul > li:nth-child(2) > div > ul > li > a")
        for i in c:
            data["writers"].append(i.text)

        # Get the stars of the movie
        d = driver.find_elements(By.CSS_SELECTOR, "div.sc-69e49b85-3.dIOekc > div > ul > li:nth-child(3) > div > ul > li > a")
        for i in d:
            data["stars"].append(i.text)

        datas.append(data)
        print("Data from " + url + " has been added to the list")

    driver.quit()
    print("Firefox Headless Browser Closed")


get_data(["https://www.imdb.com/title/tt0120737/", "https://www.imdb.com/title/tt1630029/"], driver, iterations)
print(datas)
# write datas to a json file
with open("datas.json", "w", encoding="utf-8") as file:
    json.dump(datas, file, ensure_ascii=False)