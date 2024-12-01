from glob import glob
from os.path import basename as bname
import json
from timemodes import datetime_decoder as dtd

#loads tweet data transforms date in datetime object
def loader(fname: str, conv: bool = False) -> list:
    try:
        with open(fname, "r") as fi:
            data = json.loads(fi.read())
        if conv:
            for i in range(len(data)):
                data[i]["time"] = dtd(data[i]["time"])
            return data
        else:
            return data 
    except FileNotFoundError:
        print(f"{fname} not found...")
    except Exception as e:
        print(f"Error opening {fname}: {e}")
    return []

#returns serialised tweet data for json dump string
def dumper(fname: str, data=[]) -> bool:
    try:
        with open(fname, "w") as fo:
            fo.write(json.dumps(data, indent=2))
        return True    
    except:
        return False

#return list of all accounts available in tdata folder
def get_ac_names(fpath: str = "tdata/") -> list:
    return [bname(ac).split('.')[0] for ac in glob(f"{fpath}*.json")]
    
    
#checks for and returns set of integers in a given range
#lower limit included, upper limit excluded    
def get_int(nums: list, mx: int, mn: int = 0) -> set:
    inums = set()
    for num in nums:
        num = str(num).strip('" ').strip("'")
        try:
            if mn <= int(num) < mx:
                inums.add(int(num))
        except (TypeError, ValueError):
            print(f"{num} is not a valid integer")
            continue
    return inums


#account selector from the registry list
def ac_selector() -> list:
    matches = set()
    
    names = input("Enter username(s) ',' separated and search accounts: ").split(',')
    
    ac_names = get_ac_names()
    for ac in ac_names:
        for name in names:
            if name.strip().lower() in ac.lower():
                matches.add(ac)
                break
    matches = list(matches)
    
    if matches:
        for num, ac in enumerate(matches):
            print(f" {num}.\t{ac}")
        nums = input("Enter number(s) ',' separated to select accounts: ").split(',')
        nums = get_int(nums, len(nums))
        return [matches[num] for num in nums]
    else:
        print("Not Found")
        return []      


def main():
    ...
    
if __name__ == "__main__":
    main()
