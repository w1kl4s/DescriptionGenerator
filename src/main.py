from parser import main
import sys

if len(sys.argv) == 1:
    print("You need to provide a directory!")
elif len(sys.argv) > 2:
    print("Only one directory at a time is supported! Check if the name of directory is properly formatted.")
else:
	main(sys.argv[1])
	
