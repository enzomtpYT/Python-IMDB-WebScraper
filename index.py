from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
import time, json, re, os

datas = []
options = FirefoxOptions()
# options.add_argument("--headless")
driver = webdriver.Firefox(options=options)
print("Firefox Headless Browser Invoked")
iterations = 0
doneurls=[]
t = time.localtime()
verbose = False

# Create a logger function
def log(a):
    """
    A function that logs a message if verbose is True. 
    If the log file exists, the message is appended to the file with a timestamp.
    Parameters:
        a (str): The message to be logged.
    """
    if verbose:
        log(f"[{time.strftime('%H:%M:%S', t)}] : {a}")
    if os.path.exists("log.txt"):
        with open("log.txt", "a") as file:
            file.write(f"[{time.strftime('%H:%M:%S', t)}] : {a}\n")
    else:
        with open("log.txt", "w") as file:
            file.write(f"[{time.strftime('%H:%M:%S', t)}] : {a}\n")

def get_data(urls, driver, iterations):
    """
    Get data from a list of URLs using a web driver, and iterate through the list of URLs until all data is retrieved.
    
    :param urls: list of URLs to retrieve data from
    :param driver: web driver to use for retrieving data
    :param iterations: the current iteration count
    :return: None
    """
    if iterations > 1:
        return
    print("Iteration: " + str(iterations))
    iterations+=1
    nurls = []
    for url in urls:
        if url not in doneurls:
            doneurls.append(url)
            log("Getting data from: " + url)
            data = {"title": "","year": 0,"rating": 0,"genres": []}

            driver.get(url)

            # Get the title, year, genres of the movie
            data["title"] = driver.find_element(By.CSS_SELECTOR, ".hero__primary-text").text
            data["year"] = int(driver.find_element(By.CSS_SELECTOR, "section > div > div > ul > li:nth-child(1) > a.ipc-link.ipc-link--baseAlt.ipc-link--inherit-color").text)
            try:
                data["rating"] = float(driver.find_element(By.CSS_SELECTOR, "span.sc-bde20123-1.cMEQkK").text.replace(",", "."))
            except:
                data["rating"] = 0.0

            # Get the  of the movie
            a = driver.find_elements(By.CSS_SELECTOR , "div.ipc-chip-list__scroller > a > span")
            for i in a:
                data["genres"].append(i.text)
            # Get next urls
            e = driver.find_elements(By.CSS_SELECTOR, "section:nth-child(20) > div.ipc-shoveler.ipc-shoveler--base.ipc-shoveler--page0 > div.ipc-sub-grid.ipc-sub-grid--page-span-2.ipc-sub-grid--nowrap.ipc-shoveler__grid > div > a")
            for i in e:
                url = re.sub(r"\?(.*)", "", i.get_attribute("href"))
                if url not in doneurls:
                    log("Adding " + url + " to the list")
                    nurls.append(url)
                else:
                    log(url + " is already in the list")

            datas.append(data)
            log("Data from " + url + " has been added to the list")
            nurls = nurls[0:5]
            log(nurls)
            get_data(nurls, driver, iterations)

get_data(["https://www.imdb.com/title/tt1630029/", "https://www.imdb.com/title/tt16606592/"], driver, iterations)
driver.quit()
log("Firefox Headless Browser Closed")
log(datas)
# write datas to a json file
with open("datas.json", "w", encoding="utf-8") as file:
    json.dump(datas, file, ensure_ascii=False)