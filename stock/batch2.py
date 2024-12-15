import multiprocessing
import json
import os
def process(start, end, p):
    lst = []
    print(f"Doing {p+1}")
    for i in range(start, end):
        print(f"value {i}")
        lst.append(i)
    with open(f"pool{p}.txt", 'w') as file:
        file.write(json.dumps(lst))
        
def combiner(p):
    lst = []
    i=0
    while i<p:
        with open(f"pool{i}.txt", 'r') as file:
            lst += json.loads(file.read())
        os.remove(f"pool{i}.txt")
        i+=1
    return lst
     
def main():
    total = 12
    num =2
    batch_results = []
    results = []
    for i in range(num):
        start = (total//num)*i
        end = (total//num)*(i+1)
        batch_results.append(multiprocessing.Process(target = process, args=(start, end, i)))
        batch_results[i].start()
    
    for i, b in enumerate(batch_results):
        print(f"Joining {i+1}")
        b.join()    
    print("Done")
    print(combiner(num))
    
if __name__ == "__main__":
    main()
