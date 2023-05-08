﻿#Requires AutoHotkey v2.0

colors := []
colors.Push([ "B0sh", "009ACE" ])
colors.Push([ "Lawson", "00993A" ])
colors.Push([ "Satch", "E4CB42" ])
colors.Push([ "Pablo", "CE1125" ])
colors.Push([ "James", "462376" ])
colors.Push([ "George", "1E191A" ])
colors.Push([ "Qing", "F7F577" ])
colors.Push([ "Grant", "AEE7FF" ])
colors.Push([ "Aubry", "895D94" ])
colors.Push([ "Sean", "64777D" ])
colors.Push([ "Faryn", "E17C90" ])

if (WinActive("ahk_exe Resolve.exe") and A_Args.Has(1))
{
    GetColor(name) {
        global colors

        for index, x in colors
        {
            if (name = x[1])
            {
                return x[2]    
            }
        }

        return 0
    }

    userColor := GetColor(A_Args[1])

    if (userColor != 0)
    {
        Title := WinGetTitle("A")
        if (Title = "Color") {
            CoordMode "Mouse", "Window"
            
            Click 402, 373
            Sleep 50
            Click 402, 373
            Sleep 50
            Send userColor
            Sleep 50
            Send "{Enter}"
        }

        else {
            Clipboard := userColor
        }

    }


}