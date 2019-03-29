# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys, collections

class Entry:
    def __init__(self, letter, occur, tot):
        self.letter = letter
        self.occur = occur
        self.tot = tot

    def key(self):
        return(str(self.tot - self.occur) + self.letter)


strIn = sys.stdin.read()
tot = len(strIn)
letters = {}
for c in strIn:
    if (c in letters):
        letters[c].occur += 1
    else:
        letters[c] = Entry(c, 1, tot)
#print(letters)
orderedDict = collections.OrderedDict(sorted(letters.items(), key = lambda x: x[1].key()))
i = 0
for pp in orderedDict.keys():
    i += 1
    print(f"{pp} {orderedDict[pp].occur}")
    if i >= 3: 
        break
        
