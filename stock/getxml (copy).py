import human
import atr
import json
import sys
import os
from datetime import datetime

#initialises driver
def driveop(tm=500):
    driver = human.chrome()
    driver.implicitly_wait(tm)
    return driver
        

#reads file, returns 
# list1 --> list of pending links
# list2 --> list of completed links and fetched data 
def loader(cat, year):
    links = []
    rows = []
    try:
        with open(f"{cat}_{year}_data.txt", "r") as file:
            data = json.loads(file.read())
        for d in data:
            try:
                if d['1']:
                    rows.append(d)
            except KeyError:
                links.append(d)
        return (links, rows)
    except FileNotFoundError:
        return ([], [])    
    

#clears row list by saving contents on temporary disk file
def refreshrows(rows, val):
    with open(f"temp/temp_data_{val}.txt", "w") as file:
        file.write(json.dumps(rows, indent=2))
    return []   

#fetches all temp data and returns complete row data
def completerows(frow, val):
    rows = []
    for i in range(val): 
        with open(f"temp/temp_data_{i}.txt", "r") as file:
            rows += json.loads(file.read())
        os.remove(f"temp/temp_data_{i}.txt")
    return rows + frow
    
#takes file name, fetches xml for every link in file, writes as dct in ref of atr    
def gxml(cat, year, row_size=50, driverref=300):
    links, rows = loader(cat, year)
    driver = driveop()
    #return 0
    total = len(links)
    atrv, atru = atr.getatr()
    
    print(f"{len(rows)} Done. {total} Pending... {total+len(rows)} Total")
    with open(f"{cat}_{year}_data.txt", 'w') as file:
        i, rtime = (1, datetime.now())
        for j, dct in enumerate(links):
            curr = str(i) + '.' + ' '*(len(str(total))+3 - len(str(i)))    
            print(f"{year} / {curr}{total}  ", end='')
            try:
                driver.get(dct['link'])
                xml = driver.page_source
                for kname in atrv.keys():
                    l = atrv[kname]
                    try:
                        data = xml.split(l)[1].split(">")[1].split("<")[0]
                        if kname+'u' in atru.keys() and float(data) != 0.0 or kname+'u' not in atru.keys() and len(data.strip(' '))>0:
                            dct[kname] = data
                            
                    except:
                        val = None 
                name = dct['name']
                if len(name) >= 16:
                    name = name[:15]
                else:
                    name = dct['name'] + ' '*(15 - len(dct['name']))
                print(f"{name}    ", end='')
            
            except KeyboardInterrupt:
                print(f"Closing. Line {i-1}--{dct['link']} completed...")
                
                rows = completerows(rows, i//row_size)       
                for l in range(j, len(links)):
                    rows.append(links[l])
                file.write(json.dumps(rows, indent=2))
                print(len(rows))
                driver.quit()
                sys.exit(0)
            except:
                val = None
                
            print(f"{((i)*100/total):.2f} %    {datetime.now() - rtime}")
            rows.append(dct)
            
            i += 1 
            if i % driverref == 0:
                driver.quit()
                driver = driveop()
            if i % row_size == 0:
                rows = refreshrows(rows, i//row_size-1)
                
        driver.quit()
        rows = completerows(rows, i//row_size)
        file.write(json.dumps(rows, indent=2))
        print(len(rows))
        return True

#reads broadcast date data file and writes yearly end date data file
def sortdata(fnames):
    for fname in fnames:
        with open(fname, "r") as fin:
            data = json.loads(fin.read())
    
    
               
def main():
    
    cat = "quarterly"
    sleep = True
    for year in range(23, 24): 
        gxml(cat, year)
        
    if sleep:
        os.system("systemctl suspend")
    
    print(1)
if __name__ == "__main__":
    main()
