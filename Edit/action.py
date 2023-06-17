#!/usr/bin/env python

# 18.5 undocumented functions
# https://forum.blackmagicdesign.com/viewtopic.php?f=21&t=113040

# undocumented functions
# https://gist.github.com/X-Raym/2f2bf453fc481b9cca624d7ca0e19de8?permalink_comment_id=4315832


from lib import *
from addclip import *
from getframe import *
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

    case "getframe":
        action_get_frame(dv)









