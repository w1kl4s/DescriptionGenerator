from easygui import *

def invoke_settings_window():
    msg = "settings.py file not fould!\nEnter your AniDB information here."
    title = "Enter your credentials."
    field_names = ["username", "password", "API key(optional)"]
    field_values = [] 
    field_values = multenterbox(msg,title, field_names)

    while True:
        try:
            if field_values[0] != '' and field_values[1] != '': break
        except TypeError:
            print("shit is fucked")
            raise SystemExit
        errmsg = ""
        for i in range(len(field_names)):
          if field_values[i].strip() == "":
            errmsg = errmsg + ('"%s" is a required field.\n\n' % field_names[i])
        if errmsg == "": break
        field_values = multenterbox(errmsg, title, field_names, field_values)
    with open("settings.py", 'w') as settingsfile:
        settingsfile.write("login = \"{}\"\n".format(field_values[0]))
        settingsfile.write("password = \"{}\"\n".format(field_values[1]))
        settingsfile.write("key = \"{}\"\n".format(field_values[2]))

