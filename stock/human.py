from selenium import webdriver
import os


def chrome():
    os.environ['PATH'] += r"drivers/"
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1280,800")
    #option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    option.add_argument("user-agent=Chrome/74.0.3729.169")
    #option.add_argument('proxy-server=106.122.8.54:3128')
    return webdriver.Chrome(options=option)

def firefox():
    os.environ['PATH'] += r"drivers/"
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1280,800")
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    return webdriver.Chrome(options=option)
    
def htmlparser():
    ...

def main():   
    url = "https://www.nseindia.com/companies-listing/corporate-filings-financial-results"
    driver = chrome()
    driver.get(url)
    input("Enter to collapse: ")
    

if __name__ == "__main__":
    main()
