import json

sym = "TATAMOTORS"
period = (18, 23)
mode = ["annual", "quarterly"]

vals = []
for m in mode:
    for p in range(period[0], period[1]):
        with open(f"{m}_{p}_data.txt", "r") as fi:
            tdata = json.loads(fi.read())
            for td in tdata:
                try:
                    if td["1"] == sym and "Stand" in td["23"]:
                        print(m[0],td["21"],td["50"])    
                except KeyError:
                    ...
