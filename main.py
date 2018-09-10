import sys
import os
import logging
from logging.config import fileConfig
import colorlog

from src import Parser
from src import ExceptionHandlers

try:
    import settings
except ModuleNotFoundError:
    with open("settings.py", 'w') as file:
        file.write('login = ""\n')
        file.write('password = ""\n')
        file.write('key = ""\n')
    import settings

if not settings.login or not settings.password:
    raise ExceptionHandlers.SettingsEmptyError
elif len(sys.argv) == 1:
    raise ExceptionHandlers.NoDirectoryProvided
elif len(sys.argv) > 2:
    raise ExceptionHandlers.TooManyDirectories
if __name__ == '__main__':
    path = sys.argv[1]
    folder_name = os.path.basename(os.path.dirname(path))
    fileConfig('logging_config.ini', defaults={ 'logfilename' : "logs/{}.log".format(folder_name) } )
    log = logging.getLogger()
    Parser.main(path, log)
