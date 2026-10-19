import sys
from _punctuation import normalize

if __name__ == "__main__":
    print(normalize(sys.stdin.read()), end="")
