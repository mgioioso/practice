# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys, collections

strIn = sys.stdin.read()
tot = len(strIn)
letters = {}
for c in strIn:
    if (c in letters):
        letters[c] += 1
    else:
        letters[c] = 1
#print(letters)
orderedDict = collections.OrderedDict(sorted(letters.items(), key = lambda x: str(tot - x[1])+x[0]))
i = 0
for pp in orderedDict.keys():
    i += 1
    print(f"{pp} {orderedDict[pp]}")
    if i >= 3: 
        break
        
