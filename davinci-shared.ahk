
ini(key, value)
{
    IniWrite value, "C:\YouTube\davinci.ini", "davinci", key
}

focusDavinci()
{
    ; handle being in davinci full screen mode
    if (WinActive("Resolve ahk_exe Resolve.exe") && !WinExist("DaVinci Resolve ahk_exe Resolve.exe"))
    {
        cl("In full screen, sending escape")
        Send "{Escape}"
        Sleep 250
    }

    if (!WinActive("DaVinci Resolve ahk_exe Resolve.exe"))
    {
        cl("Activating dv")
        WinActivate("DaVinci Resolve ahk_exe Resolve.exe")
        Sleep 100
    }
}

runScript(action, content)
{
    focusDavinci()    
    ini("action", action)
    ini("content", content)
    Sleep 100

    ; Send "\"

    MouseGetPos &xpos, &ypos
    if (imageClick("images/resolve-workspace.png"))
    { 
        Send "{Up}"
        Send "{Right}"
        Send "{Down}"
        Send "{Enter}"
        MouseMove xpos, ypos
    }

}

imageClick(path, offsetX := 0, offsetY := 0)
{
    try
    {
        CoordMode "Mouse", "Client"
        if (ImageSearch(&FoundX, &FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight, "*8 " path))
        {
            Click FoundX + offsetX, FoundY + offsetY
            Return True
        }
    }
    catch as exc
    {
        MsgBox "Could not conduct the search due to the following error:`n" exc.Message
    }

    Return False
}

cl(text, overwrite := false) {
    if (overwrite) {
        FileDelete("log.txt")
    }
    FileAppend(text "`n", "log.txt")
}
cl(A_Now, true)