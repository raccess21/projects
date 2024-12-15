import os
import json
from bs4 import BeautifulSoup as bs
def reader(fname):
    with open(fname, "r") as file:
        data = file.read()
    return data

#html data to list of dict    
def p2(dps):
    lst, num, sp = ([], 0, "https://nsearchives.nseindia.com/corporate")
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
            lst.append(dct)
            num += 1
    print(f'Fetched {num} out of {len(dps.split("nsearchives.nseindia.com/corporate"))-1}...')
    return lst
        
        
def dumper(datalst):
    for ent in datalst:
        ...

def main():      
    fname = "quarterly_23"#input("Enter file name: ")
    
    with open(fname+'.txt', "r") as fi:
        data = fi.read()
    data = p2(data)
    with open(fname+'_data.txt', "w") as fo:
        fo.write(json.dumps(data, indent=2))
if __name__ == "__main__":
    main()
