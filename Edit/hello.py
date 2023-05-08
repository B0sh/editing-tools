#!/usr/bin/env python

# undocumented functions
# https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=113040

from lib import *
from addclip import *
import configparser
import inspect
from datetime import datetime

config = configparser.ConfigParser()
config.read("C:\\YouTube\\davinci.ini", encoding="utf16")

dv = get_dv(app, config['davinci']['action'], config['davinci']['content'])

print("")
print("")
print(" -------- B0sh Davinci Script -------- ")
print(" --- ", datetime.now())
print(" ---  Action:", dv.action)
print(" ---  Content:", dv.content)
print("")


match dv.action:
    case "addsfx":
        action_add_sfx(dv)

    case "addclip":
        action_add_clip(dv)

    case "addnewclip":
        action_add_new_clip(dv)









