import json

#a = all, u = unit, v = values
def getatr(mode='a'):
    with open("atr.txt", "r") as file:
        atr = json.loads(file.read())
    if mode == 'u':
        return atr[1]
    elif mode == 'v':
        return atr[0]
    else:
        return atr

    
#prints attributes/keys present in xml file
def createatr(xml, sp="/in-bse-fin:"):
    dct = {}
    dctu = {}
    for i, label in enumerate(str(xml).split(sp)[:len(xml.split(sp))-1]):
        dct[f"{i}"] = label.split('in-bse-fin:')[1].split(' ')[0]
        if 'unitRef' in label:
            dctu[f"{i}u"] = label.split('unitRef=')[1].split(' ')[0].strip('"') 
    return [dct, dctu]
    

def writeatr(dct, temp=True):
    if temp:
        fname = "temp.txt"
    else:
        fname = "atr.txt"
    with open(fname, 'w') as file:
        file.write(json.dumps(dct, indent=2))
    
    
def updateatr(xml, temp=True):
    oldatr, newatr = (getatr('a'), createatr(xml))
    okeynames = [oldatr[0][key] for key in oldatr[0].keys()]
    okeys = len(okeynames)
    
    i = 0
    for nkey in newatr[0].keys():
        if newatr[0][nkey] not in okeynames:
            oldatr[0][f"{okeys+i}"] = newatr[0][nkey]
            try:
                oldatr[1][f"{okeys+i}u"] = newatr[1][nkey+'u']
            except KeyError:
                ...
            i += 1
    writeatr(oldatr, False)
    
xml = '<in-bse-fin:DescriptionOfSingleSegment contextRef="OneD">CAPITAL MARKET OPERATIONS</in-bse-fin:DescriptionOfSingleSegment>'
updateatr(xml)

