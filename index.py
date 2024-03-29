from selenium import webdriver
from selenium.webdriver.firefox.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
import time, json, re, os

datas = []
options = ChromeOptions()
# options.add_argument("--headless")
driver = webdriver.ChromiumEdge(options=options)
print("Chrome Headless Browser Invoked")
t = time.localtime()
verbose = True
genres = ["Action", "Adventure", "Animation", "Biography", "Comedy", "Crime", "Drama", "Family", "Fantasy", "Film-Noir", "Game-Show", "History", "Horror", "Music", "Musical", "Mystery", "Romance", "Sci-Fi", "Sport", "Thriller", "War", "Western"]

# Create a logger function
def log(a):
    """
    A function that logs a message if verbose is True. 
    If the log file exists, the message is appended to the file with a timestamp.
    Parameters:
        a (str): The message to be logged.
    """
    if verbose:
        print(f"[{time.strftime('%H:%M:%S', t)}] : {a}")
    if os.path.exists("log.txt"):
        with open("log.txt", "a") as file:
            file.write(f"[{time.strftime('%H:%M:%S', t)}] : {a}\n")
    else:
        with open("log.txt", "w") as file:
            file.write(f"[{time.strftime('%H:%M:%S', t)}] : {a}\n")

def get_data(genres, driver):
    data = {}
    for genre in genres:
        log(f"Getting data for {genre}")
        driver.get(f"https://www.imdb.com/search/title/?title_type=feature&genres={genre}%2C%21documentary%2C%21short")
        for i in range(1, 51):
            name = driver.find_element(By.CSS_SELECTOR, f"li:nth-child({i}) > div > div > div > div.sc-d80c3c78-3.gqHsYK > div.sc-b0691f29-0.jbYPfh > div.ipc-title.ipc-title--base.ipc-title--title.ipc-title-link-no-icon.ipc-title--on-textPrimary.sc-b0691f29-9.klOwFB.dli-title > a > h3").text
            name = re.sub(r".*.\..", "", name)
            try:
                data[name] = {
                    "year": driver.find_element(By.CSS_SELECTOR, f"li:nth-child({i}) > div > div > div > div.sc-d80c3c78-3.gqHsYK > div.sc-b0691f29-0.jbYPfh > div.sc-b0691f29-7.hrgukm.dli-title-metadata > span:nth-child(1)").text
                }
            except:
                data[name]["year"] = {
                    "year": "0"
                }
            try:
                data[name]["rating"] = driver.find_element(By.CSS_SELECTOR, f"li:nth-child({i}) > div > div > div > div.sc-d80c3c78-3.gqHsYK > div.sc-b0691f29-0.jbYPfh > span > div > span").text
            except:
                data[name]["rating"] = "0.0"
            if "genres" in data[name]:
                data[name]["genres"].append(genre)
            else:
                data[name]["genres"] = [genre]
            log(f"{name} : {data[name]}")
    datas.append(data)

get_data(genres, driver)
driver.quit()
log("Chrome Headless Browser Closed")
log(datas)
# write datas to a json file
with open("datas.json", "w", encoding="utf-8") as file:
    json.dump(datas, file, ensure_ascii=False)