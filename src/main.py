import sys
import logging
from logging.config import fileConfig

from parser import main
from exceptionhandlers import NoDirectoryProvided, TooManyDirectories

fileConfig('src/logging_config.ini')
log = logging.getLogger()
logging.basicConfig(filename='myapp.log', level=logging.INFO)

if len(sys.argv) == 1:
    log.error("No directory provided.")
    raise NoDirectoryProvided
elif len(sys.argv) > 2:
    log.error("Too Many Directories")
    raise TooManyDirectories
if __name__ == '__main__':
    main(sys.argv[1], log)
