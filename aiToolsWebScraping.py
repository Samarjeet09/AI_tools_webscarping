from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import Keys
import requests
import time
import bs4
import pandas as pd
from tqdm import tqdm


baseLink = "https://topai.tools"
d = {
    "tool_name": [],
    "tool_url": [],
    "description": [],
    "pricing": [],
    "tag": [],
    "use_cases": [],
}

driver = webdriver.Chrome()
driver.get("https://topai.tools/browse")
# scroll down to end of page
html = driver.find_element(By.TAG_NAME, "html")
for i in tqdm(range(500),position=0, leave=True):
    time.sleep(0.7)
    html.send_keys(Keys.END)

pageHtml = driver.page_source
soup = bs4.BeautifulSoup(pageHtml, "html.parser")

print("Done Scrolling no of blocks found:")
block = soup.findAll("div", {"class": "tool-wrapper"})
print(len(block))

print("Exploring items")
for item in tqdm(block):
    t = item.a["href"]
    if t == "#":
        continue
    # print(t)
    # make req for each page
    try:
        req = requests.get(baseLink + t)
    except:
        continue
    else:
        soup2 = bs4.BeautifulSoup(req.text, "html.parser")
        try:
            name = soup2.find_all("h1")[0].text.strip()
            tool_link = soup2.findAll("i", {"class": "bi bi-box-arrow-up-right mx-2"})[
                0
            ].parent["href"]
        except:
            continue
        else:
            try:
                what_is = soup2.findAll("p", {"class": "p-1 py-2 rounded"})[
                    0
                ].text.strip()
            except:
                what_is = ""
            try:
                pricingAndTagged = soup2.findAll("small", {"class": "text-app"})
                pricing = pricingAndTagged[0].next.next.next.text.strip()
                tagged = ""
                for tags in pricingAndTagged[1].parent.findAll("span"):
                    tagged += tags.text.strip() + ","
                tagged = tagged[:-1]
            except:
                pricing = ""
                tagged = ""
            try:
                useCases = soup2.findAll("ol")[0].text.strip()
            except:
                useCases = ""
            d["tool_name"].append(name)
            d["tool_url"].append(tool_link)
            d["description"].append(what_is)
            d["pricing"].append(pricing)
            d["tag"].append(tagged)
            d["use_cases"].append(useCases)


df = pd.DataFrame(d)
df.to_excel("output.xlsx")


driver.quit()
