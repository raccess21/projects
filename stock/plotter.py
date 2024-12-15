import matplotlib.pyplot as plt
import numpy as np
import json
from atrlst import xml25dct

#returns list of keys for analysis
def anakey():
    return [
        #'19', #date of end
        '22',  # rev from op
        '28',  # employee benefit expense
        '50',  # profit before tax
        '38',  # tax expense
        #'106', # debt equity ratio
    ]
#returns raw company data from specified file path
def rcdata(fpath):
    with open(fpath, "r") as f:
        return json.loads(f.read())

'''
[{
    "date": [],
    "22": [],
}]
'''
def line_graph(dct):
    for i in range(len(ftype)):
        fdct[i]['19'].reverse()
        xp = np.array(fdct[i]['19'])
        for key in anakey():
            fdct[i][key].reverse()
            yp = np.array(fdct[i][key])
            plt.plot(xp, yp, label = xml25dct()[key].split(':')[1])
        plt.title(f"Quarterly report data '{name}' ({ftype[i]})")
        plt.xlabel("Time - Period")
        plt.ylabel("Amount (in Crores)")
        plt.xticks(rotation=45)
        plt.legend()
        plt.tight_layout()
        #plt.savefig(f"data/graphs/{name}.png")
        plt.show()

def pl():
    names = ["GISOLUTION",]#"TCS", "ADANIENT", "TATASTEEL", "TATAPOWER", "ADANIPOWER"]
    for name in names:
        fdata = rcdata(f"data/data/quarter/{name}.txt")
        fdct = [{},{}]
        fdct[0]['19'] = []
        fdct[1]['19'] = []
        ftype = ["standalone", "consolidated"]
        for i in range(len(ftype)):
            for key in anakey():
                fdct[i][key] = []
        for dct in fdata:
            if dct['21']:
                dct['21'] = dct['21'].lower()
            if dct['21'] == ftype[0]:
                i = 0
            else:# dct['21'] == ftype[1]:
                i = 1
            if dct['19']:
                fdct[i]['19'].append(dct['19'][2:])
            else:
                fdct[i]['19'].append("404")
            for key in anakey():
                if dct[key]:
                    fdct[i][key].append(float(dct[key])/10000000)
                else:
                    fdct[i][key].append(None)
        for i in range(len(ftype)):
            fdct[i]['19'].reverse()
            xp = np.array(fdct[i]['19'])
            for key in anakey():
                fdct[i][key].reverse()
                yp = np.array(fdct[i][key])
                plt.plot(xp, yp, label = xml25dct()[key].split(':')[1])
            plt.title(f"Quarterly report data '{name}' ({ftype[i]})")
            plt.xlabel("Time - Period")
            plt.ylabel("Amount (in Crores)")
            plt.xticks(rotation=45)
            plt.legend()
            plt.tight_layout()
            #plt.savefig(f"data/graphs/{name}.png")
            plt.show()
