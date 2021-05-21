import sys

def printCommands():
    print("1. python run.py all (or --all) for run all files")
    print("2. python run.py filename (or --filename), to calculate multiple files write them space seperated")

if len(sys.argv) < 2:
    raise Exception("No file mentioned, please use --help or help to see list of commands")
if "--help" in sys.argv or "help" in sys.argv:
    printCommands()

allFiles = ["aHash", "--aHash", "dHash", "--dHash"]


