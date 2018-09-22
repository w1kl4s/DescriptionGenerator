import sys
import os
import easygui
import logging
from logging.config import fileConfig
import colorlog

from src import Parser
from src import ExceptionHandlers
from src import SettingsGUI
try:
    import settings
except ModuleNotFoundError:
    SettingsGUI.invoke_settings_window()
    import settings

if not settings.login or not settings.password:
    raise ExceptionHandlers.SettingsEmptyError
elif len(sys.argv) > 2:
    raise ExceptionHandlers.TooManyDirectories
elif len(sys.argv) == 1:
    path = easygui.diropenbox()
    if path == None:
        raise ExceptionHandlers.NoDirectoryProvided
else:
    path = sys.argv[1]
if __name__ == '__main__':
    folder_name = os.path.basename(os.path.dirname(path))
    folder_name = folder_name.replace("\'","")
    folder_name = folder_name.replace("\"","")
    fileConfig('logging_config.ini', defaults={ 'logfilename' : "logs/{}.log".format(folder_name) } )
    log = logging.getLogger()
    Parser.main(path, log)
