import human
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from  time import sleep
from files import loader, dumper
from random import uniform


#input value in randomised manner
def slowenter(val, ele):
    for v in val:
        sleep(round(uniform(0, 0.3), 2)) 
        ele.send_keys(v)
        

#login twitter account detais   
#user -> {"uname": username, "pass": password}     
def login(driver, user: dict) -> bool:
    url = "https://twitter.com/" + "home"
    
    driver.implicitly_wait(100)
    driver.get(url)
    try:
        slowenter(user['uname'], driver.find_element(By.CLASS_NAME, "r-30o5oe"))
        driver.find_element(By.XPATH, "//span[text()='Next']").click()
        slowenter(user['pass'], driver.find_elements(By.CLASS_NAME, "r-30o5oe")[1])
        driver.find_element(By.XPATH, "//span[text()='Log in']").click()
        print("Login Complete: ")
        if url == driver.current_url:
            return True
        else:
            print("Login error: ")
            
    except Exception as e:
        print(f"Error {e}")
    
    return False   

#scrapes tweet and saves in file in list of dict form
#[{"link", link_of_tweet, "time", time_of_tweet, "tweet": tweet_text, "status":status}, {}...]
def ptweet(driver, name: str, wait_time: int) -> list:
    url = "https://twitter.com/" + name
    tweetBody = '[data-testid="cellInnerDiv"]'                          #tweets list css selector
    tweetText = '[data-testid="tweetText"]'                             #tweet text css selector 
    completion_status = '[data-testid="tweet-text-show-more-link"]'     #tweet text complete or not
    
    #load existing tweets from local file 
    #if not tweet present otweets is initialised with empty list
    fpath = f"tdata/{name}.json"
    otweets = loader(fpath)
    i = 0
    
    try:
        driver.implicitly_wait(wait_time)
        driver.get(url)
    except Exception as e:
        print(f"Error fetching {url}:  {e}")
        return []
    finally:
        if url != driver.current_url:
            print("Invalid account")
            return False
    #scrape tweets until keyboard interrupt
    curr_scroll = driver.execute_script("return window.pageYOffset;")
    while True:
        try:    
            driver.implicitly_wait(wait_time)
            tweets = driver.find_elements(By.CSS_SELECTOR, tweetBody)
            
            olinks = [otweet["link"] for otweet in otweets]
            #new tweets are loaded at the end of list
            #reversed for quicker new tweet retrieval 
            #if duplicate tweet then break and retrieve list of tweets again
            driver.implicitly_wait(wait_time/50)
            
            for tweet in reversed(tweets):
                dct = {}
                try:
                    samay = tweet.find_element(By.TAG_NAME, "time")
                    dct["link"] = samay.find_element(By.XPATH, "./parent::a").get_attribute("href")
                    if dct["link"] not in olinks:
                        try:
                            dct["time"] = samay.get_attribute("datetime").split(".")[0]
                            try:
                                dct["tweet"] = tweet.find_element(By.CSS_SELECTOR, tweetText).text
                            except NoSuchElementException:
                                dct["tweet"] = ''
                            try:
                                tweet.find_element(By.CSS_SELECTOR, completion_status)
                                dct["status"] = False
                            except NoSuchElementException:
                                dct["status"] = True
                            otweets.append(dct)
                            i += 1
                            print(f"{i}. {dct['link']}", {dct['tweet'].split('\n')[0].split('.')[0]})
                        except NoSuchElementException:
                             ...
                        
                    else:
                        break
                    
                except Exception as e:
                    print(f"tweet in tweets error: {e}")
            
        except (KeyboardInterrupt, EOFError):
            print(f"\nWriting data in tdata\{name}.json...")
            dumper(fpath, otweets)
            return otweets
        except Exception as e:
            print(f"tweets block error :{e}") 
            break
        finally:
            sleep(round(uniform(0.2, 0.5),2)) 
            driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)            
            if curr_scroll == driver.execute_script("return window.pageYOffset;"):
                try:
                    driver.find_element(By.XPATH, "//span[text()='Not now']").click()
                    driver.find_element(By.TAG_NAME, 'body').send_keys(Keys.PAGE_DOWN)            
                    
                except:
                    ...
                sleep(2)
                if curr_scroll == driver.execute_script("return window.pageYOffset;"):
                    print("End of page")
                    break
            else:
                curr_scroll = driver.execute_script("return window.pageYOffset;")
    dumper(fpath, otweets)
    return otweets
            
def getdriver():
    #os.environ['PATH'] += r"drivers/"
    driver = human.chrome_human()
    return driver

def scrape(**args):
    names = input("Enter exact usernames (, separated) to fetch tweets from: ").split(',')
    
    driver = getdriver()
    if args["user"]:
        login(driver, user)
    for i, name in enumerate([name.strip(', ') for name in names]):   
        print(f"Scraping {i+1}. {name}...") 
        ptweet(driver, name, args["wait_time"])
    driver.quit()
    input("Scraping Complete. Press enter.")
 
    
def main():
    driver = getdriver()
    ptweet(driver, "rasbdi2378dcjefg86243fjhhf")
    print(f"%^%^%^%^")
    
if __name__ == "__main__":
    main()
