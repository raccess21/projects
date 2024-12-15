import time
import json
from bs4 import BeautifulSoup as bs
from datetime import date
from lxml import etree
def algo1():
    name = input("Enter symbol: ").upper()
    cat = ["annual", "quarterly"]
    for i in range(18, 23):
        for c in cat:    
            with open(f"{c}_{i}_data.txt", "r") as file:
                data = json.loads(file.read())
            for d in data:
                if d["1"] == name:
                    try:
                        print(f"{c[:5]}\t{d['21']}: {d['22']}\t{d['23']}\t{d['106']}")
                    except KeyError:
                        ...
                        
def sort():
    cat = ["quarterly"]#["annual"]#, 
    for c in cat:        
        years = {f"{i}": [] for i in range(10, 23)}
        for i in range(18, 23):
            with open(f"{c}_{i}_data.txt", "r") as file:
                for d in json.loads(file.read()):
                    try:
                        year = d["6"].split("-")[0][2:]
                        years[year].append(d)
                    except KeyError:
                        print(f"{c}\t{i}\t{d}")
                        #input("Error enter: ")
        for i in range(10, 23):
            with open(f"data/{c}_{i}.txt", "w") as file:
                file.write(json.dumps(years[str(i)], indent=2))                    
 
def p1(dps):
    print(len(dps.split("nsearchives.nseindia.com/corporate"))-1)
    soup = bs(dps, "lxml")            
    #trs = soup.find("tbody").find_all("tr")
    trs = soup.xpath("//tbody")
    for i, tr in enumerate(trs):
        print(i+1)

    
def p2(dps):
    lst, num, sp = ([], 0, "nsearchives.nseindia.com/corporate")
    atrlst = ["name", "cum", "cat", "rlt"]
    ilst = [0, 2, 5, 6]
    for tr in dps.split("<tr>")[1:]:
        if sp in tr:
            dct = {}
            tds = bs(tr.split("/tr>")[0].split("<table")[0] + "</td>", "html.parser").find_all("td")
            for i in range(len(atrlst)):
                try:
                    dct[atrlst[i]] = tds[ilst[i]].text
                except:
                    dct[atrlst[i]] = 0
                            
            dct['link'] = sp + tr.split(sp)[1].split(" ")[0].strip('"')
            if len(dct['cum']) > 11:
                dct['cum'] = 0    
            
            dct['bd'] = tds[len(tds)-1].text
            print(dct, end='\n\n')    
            lst.append(dct)
            num += 1
    print(f'Fetched {num} out of {len(dps.split("nsearchives.nseindia.com/corporate"))-1}...')

def namelst(nnamelst):
    with open("name.txt", "r") as file:
        onamelst = json.loads(file.read())
    onames = [i['name'] for i in onamelst]    
    for nname in nnamelst:
        ...
        
p2(reader("temp.txt"))
