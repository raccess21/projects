from selenium import webdriver
import os

def chrome_human():
    os.environ['PATH'] += r"drivers/"
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1280,800")
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    option.add_argument("user-agent=Chrome/74.0.3729.169")
    return webdriver.Chrome(options=option)

def firefox_human():
    os.environ['PATH'] += r"drivers/"
    option = webdriver.ChromeOptions()
    option.add_argument('--disable-blink-features=AutomationControlled')
    option.add_argument("window-size=1280,800")
    option.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36")
    return webdriver.Firefox(options=option)

def main():   
    ...

if __name__ == "__main__":
    main()
