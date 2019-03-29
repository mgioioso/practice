# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys, collections
import pandas as pd

class Entry:
    def __init__(self, letter, occur, tot):
        self.letter = letter
        self.occur = occur
        self.tot = tot

    def key(self):
        return(str(self.tot - self.occur) + self.letter)


strIn = sys.stdin.read()
tot = len(strIn)
df = pd.Series(list(strIn)[0:-1]) # remove newline


print(df)
df2 = df.value_counts()
df2.index
#df2.reindex(
print(df2)

        
