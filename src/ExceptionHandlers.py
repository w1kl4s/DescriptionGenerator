class NoDirectoryProvided(Exception):
    def __init__(self):
        self.message = "You need to provide a directory!"
    def __str__(self):
        return self.message

class TooManyDirectories(Exception):
    def __init__(self):
        self.message = "Only one directory at a time is supported! Check if the name of directory is properly formatted."
    def __str__(self):
        return self.message

class AniDBDown(Exception):
    def __init__(self):
        self.message = "AniDB seems to be down."
    def __str__(self):
        return self.message
class AniDBResponseException(Exception):
    def __init__(self, response_code):
        self.response_code = response_code
    def __str__(self):
        return "Wrong response code! Query doesn't exist! Response code: {}".format(self.response_code)
class ReleaseCheckException(Exception):
    def __init__(self):
        self.message = "Release check failed! Either resolution, anime id or group id don't match for all files!"
    def __str__(self):
        return self.message
class FileCountError(Exception):
    def __init__(self):
        self.message = "Verification failed!\nFile count in directory is lower than number of episodes on AniDB!" \
                       " Maybe your version is missing something?"
    def __str__(self):
        return self.message
class LogoutError(Exception):
    def __init__(self):
        self.message = "Logout Failed! Maybe network connection changed during runtime?"
    def __str__(self):
        return self.message
class HTTPApiError(Exception):
    def __init__(self):
        self.message = "HTTP Api returned wrong response! Either file information is really fucked, or client got banned! Try again in few hours."
    def __str__(self):
        return self.message
class SettingsEmptyError(Exception):
    def __init__(self):
        self.message = "Settings file was empty. This is expected on first run. Fill settings.py file with AniDB credetials and try again."
    def __str__(self):
        return self.message
