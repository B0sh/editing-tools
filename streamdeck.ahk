#Requires AutoHotkey v2.0
#Include davinci-shared.ahk

if (A_Args[1] == "player")
{
    IniWrite A_Args[2], "player.ini", "davinci", "player"
}
else if (A_Args[1] == "action") 
{
    player := IniRead("player.ini", "davinci", "player")

    switch (A_Args[2]) 
    {
        case "color":
            PlayerColor(player)
        case "face":
            player := ImageName(player)
            runScript("addclip", player . "-face.png")
        case "full":
            player := ImageName(player)
            runScript("addclip", player . "-full.png")
        case "subtitle":
            player := ImageName(player)
            runScript("addclip", player . "-subtitle.png")
        case "overlay":
            player := ImageName(player)
            runScript("addclip", player . "-overlay.png")
        case "gamesound":
            updateTracksForGameSound()
    }
}

ImageName(player) {
    if (player == "Lawson") {
        return "TheKingJock"
    }
    if (player == "Satch") {
        return "GoldenBagon"
    }
    if (player == "Pablo") {
        return "Catholoco"
    }
    if (player == "Faryn") {
        return "Farynheight"
    }
    return player
}

GetColor(name) {
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
    colors.Push([ "Elwyn", "E475FF" ])

    for index, x in colors
    {
        if (name = x[1])
        {
            return x[2]    
        }
    }

    return 0
}


PlayerColor(player) {
    userColor := GetColor(player)
    if (userColor == 0)
    {
        Return
    }

    if (WinActive("DaVinci Resolve ahk_exe Resolve.exe"))
    {
        MouseGetPos &xpos, &ypos
        CoordMode "Mouse", "Client"

        Title := WinGetTitle("A")
        if (Title != "Color")
        {
            if (!imageClick("images/resolve-color.png", 75, 10))
            { 
                Return
            }
        }

        Loop 20 {
            Title := WinGetTitle("A")
            if (Title = "Color")
            {
                Click 391, 341, 2
                Sleep 50
                Send userColor
                Sleep 50
                Send "{Enter}"
                MouseMove xpos, ypos
                Return
            }
            Sleep 50
        }

        MouseMove xpos, ypos
    }
    else
    {
        Clipboard := userColor
    }
}

updateTracksForGameSound()
{
    if (WinActive("DaVinci Resolve ahk_exe Resolve.exe"))
    {
        Send "!a"
        Sleep 300
        Click 239, 54 ; audio tab
        Sleep 100
        Click 78, 187 ; format
        Sleep 100
        Send "s{Enter}" ; select stereo

        Sleep 100
        Click 259, 185
        Sleep 100
        Send "Embedded Channel 5{Enter}"
        Sleep 100

        Click 259, 212
        Sleep 100
        Send "Embedded Channel 6{Enter}"
        Sleep 100

        Send "{Enter}"
    }
}