import glob
import os
import json


def (fname):
    with open(fname, 'r') as fi:
        return json.loads(fi.read())
        
def update(fname, ndata):
    try:
        with open(fname, "r") as fi:
            odata = json.loads(fi.read())
            
    except FileNotFoundError:
        with open(fname, "w") as fo:
            fo.write(json.dumps(ndata, indent=2))
        return True
    except:
            return False  
    inc = []
    names = []
    rpath = "data/data/quarter/"
    with open("file2.txt", "r") as f:
        for name in f.readlines():
            names.append(rpath + name.split(',')[1] + ".txt")
    names = sorted(names)
    fpaths = sorted(glob.glob(os.path.join(f"{rpath}", "*.txt")))   

    fpn = 0
    for i in range(len(names)):
        fails = 1
        for j in range(len(fpaths)):
            if names[i] == fpaths[j]:
                fails = None
                fpn = j+1
                break
        if fails:
            inc.append(names[i].split(rpath)[1])
            
    print(len(inc))           
    print(len(fpaths))           
    print(len(names))

    with open("inc.txt", "w") as f:
        for name in inc:
            f.write(f"1,{name},1\n")
            
def main():
    cnames()
    
    
if __name__ == "__main__":
    main()
