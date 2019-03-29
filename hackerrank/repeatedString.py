# Enter your code here. Read input from STDIN. Print output to STDOUT
import sys, math


def repeatedString(s, n):
  
    lens = len(s)
    modn = n % lens
    natot = 0
    nashort = 0
    i = 0
    for c in s:
        i = i + 1
        if (c=="a"):
            natot = natot + 1
            if (i <= modn):
                nashort = nashort + 1

    return natot * math.ceil(n/lens) + nashort

  
if __name__== "__main__":
    args = sys.stdin.readlines()
    s = args[0]
    n = int(args[1])
      
    print(repeatedString(s, n))

