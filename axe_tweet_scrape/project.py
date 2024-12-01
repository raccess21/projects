import sys
from timemodes import tperiod, in_interval
from files import ac_selector, loader, get_int
from tscrape import scrape
import re
import os
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as dt


def main():
    main_menu()
    

#creates folders if not already present
#graphs -> save pyplot graphs
#tdata -> save tweet data
def initialise_folder():
    for folder in ["graphs", "tdata"]:
        os.makedirs(folder, exist_ok=True)  
    
    
def main_menu():
    initialise_folder()
    i = False
    while True:
        os.system("clear")
        if i:
            print("Invalid choice")
            i = False
        print("Input Menu")
        print("1. Scrape Tweets :  ")
        print("2. Analyse Tweets: ")
        
        match input("3. Exit (1/2/3)  : "):
            case '1':
                scrape_menu()
            case '2':
                analyse_menu()
            case '3':
                break
            case _:
                i = True
    print("Exiting...")
    sys.exit(0.5)

def scrape_menu():
    user = {}
    print("This is tweet scrape menu.")
    print("1. Without login (100 tweet/person limit)")
    while True:
        try:
            match input("2. Login (More tweets more filters) (1/2): "):
                case '1':
                    break
                case '2':
                    user["uname"] = input("Enter username or email: ")
                    user["pass"]  = input("Enter username or email: ")  
                    break  
                case _:
                    print("Invalid choice: ")
        except KeyboardInterrupt:
            return None
    try:
        wait_time = int(input("Enter wait time in seconds: "))
    except:
        wait_time = 50      
    scrape(user=user, wait_time=wait_time)
    input("Press enter and exit srape: ")
    return True    


def analyse_menu():
    save = input("Save result graphs (y/n): ")[0].lower() == 'y'
    words = input("Enter list of words (, separated): ").split(",")
    words = [word.strip() for word in words]
    dates = None
    while True:
        mode = input("Enter mode (ranged/all): ")[0].lower()
        if mode == 'r': 
            dates = tperiod()
            break
        elif mode == 'a':
            break
    data = dict()
    for fname in [ac for ac in ac_selector()]:
        data[fname] = loader(f"tdata/{fname}.json", True)
    if data:
        if dates:
            cdata = calc_word_time(words, data, dates)
            plot_word_time(cdata, dates, save)
        else:
            cdata = calc_word_volume(words, data)
            plot_word_volume(cdata, save)
    else:
        print("No existing account selected...")
        
        
#---------------------data analysis functions-------------------------------#

#returns the count of the occurence of word in given sample of string data
#ignores -> case
#counts  -> word, word surrounded by quotes e;g counts shyam and Shyam's 
#           or plurals or hyphens and slashed
def occurence(word: list, data: str) -> int:
    if word:
        try:    
            data = str(data)
            pattern = r"(?:^|[\s\W]){}(?:$|[s\s\W])".format(re.escape(word))
            return len(re.findall(pattern, data, flags=re.IGNORECASE))
        except Exception as e:
            print(e)
    return 0



#calculate total instances of use of word throughout database
#data -> {user1: [list of data1], user2: [data2]...}
#returns dict of word and their counts {user1:{"word": count -> int}, user2:{}....
def calc_word_volume(words: list, data: dict) -> dict:
    cdata = dict()
    for user in data.keys():    
        wordsc = {word: 0 for word in words}
        for word in words:
            count = 0
            for d in data[user]:
                count += occurence(word, d["tweet"])
            wordsc[word] = count
        cdata[user] = wordsc
    return cdata


#calculate use of word as a function of time for every user account in list
#data -> {user1: [list of data1], user2: [data2]...}
#returns -> {user1: {word: wordcount}, user2:{word: wordcount}...}
def calc_word_time(words: list, data: dict, dates: list) -> dict:
    cdata = dict()
    for user in data.keys():
        pltarr = {word: [0] for word in words}
        for word in words:
            for i in range(len(dates)-1):    
                count = 0
                for d in data[user]:
                    if in_interval(d["time"], dates[i], dates[i+1]):
                        count += occurence(word, d["tweet"])
                pltarr[word].append(count)
        cdata[user] = pltarr 
    return cdata

    
#------------------data visualisation plot functions---------------------------#

def saver(name: str, plt) -> bool:
    now = re.sub(r'\D', '_', str(dt.now()))
    name = f"graphs/{name}_{now}.png"
    plt.savefig(name)
    return True

def get_words(cdata: dict) -> list:
    words = []
    for user in cdata.keys():
        for word in cdata[user].keys():
            words.append(word)
        break
    return words
             
#bar grapgh plotter
#words -> list of words for and 
#cdata-> dict of key -> users and value -> dict of {word1: word_count1, ...} 
def plot_word_volume(cdata: dict, save: bool = False) -> bool:
    words = get_words(cdata)
    
    # Create a bar graph
    #bar_width available 1 / 1 more than total users to avoid overlap
    bar_width = 1/(len(cdata.keys())+1)
    bar_pos = np.arange(len(words))
    
    try:
        for i, user in enumerate(cdata.keys()):
            values = [cdata[user][word] for word in words]
            pos = bar_pos + i * bar_width
            plt.bar(pos, values, width=bar_width, label=f"{user}")   
            
            #write value of bar on top of bar
            for x, value in zip(pos, values):
                plt.text(x, value+0.5, str(value), ha="center", va="center") 

        # Add labels and title
        plt.xlabel('Words --->')
        plt.ylabel('Times Used --->')
        plt.title('Volume of Word use by accounts'.title())
        
        # Add legends
        plt.legend()

        # Set x-axis tick positions and labels
        plt.xticks(bar_pos + i*bar_width/2, words)

        if save:    
            saver("bar_all", plt)

        # Show the plot
        plt.show()
        input("Press Enter to collapse graphs.")
        plt.close()
        return True
    except Exception as e:
        print(f"Error {e}")
        return False


#line grapgh plotter
#cdata -> dict of users and words for and count of their use over time for all users
#dates -> time period points
def plot_word_time(cdata: dict, dates: list = None, save: bool = False) -> bool:
    if not dates:
        return plot_word_volume(cdata, save)
    
    xp = np.array(dates)
    words = get_words(cdata)
    users = [user for user in cdata.keys()]
    try:
        for i, user in enumerate(users):
            for word in words:
                yp = np.array(cdata[user][word])
                for j, ch in enumerate([i, len(users)]):
                    plt.figure(ch)
                    plt.plot(xp, yp, label=word)
                    for xi, yi in zip(xp, yp):
                        if str(yi) != '0' and j == 0:
                            plt.text(xi, yi, yi)
                    word += f"->{user}"
                
                    plt.title(f'{j+1}. {user.title()}')
                    plt.xlabel("Time (Date)  --->")
                    plt.ylabel("Use frequency (Times) --->")
                    plt.xticks(rotation=45)
                    plt.legend()
                    plt.tight_layout()
                    

        plt.figure(len(users))
        plt.title(f'{len(users)}. All')
        users.append("All")
        if save:
            for i, name in enumerate(users):
                plt.figure(i)
                saver("line_"+name, plt)
        
        # Show the plots
        plt.show()
        input("Press Enter to collapse graphs.")
        plt.close()
        return True
        
    except Exception as e:
        print(f"Error {e}")
    return False
   


#!------------!!-----------!!___________!!--------------!!---------------!#   

if __name__ == "__main__":
    main()
