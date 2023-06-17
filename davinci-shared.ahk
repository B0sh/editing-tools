
ini(key, value)
{
    IniWrite value, "C:\YouTube\davinci.ini", "davinci", key
}

focusDavinci()
{
    ; handle being in davinci full screen mode
    if (WinActive("Resolve ahk_exe Resolve.exe") && !WinExist("DaVinci Resolve - ahk_exe Resolve.exe"))
    {
        cl("In full screen, sending escape")
        Send "{Escape}"
        Sleep 250
    }

    if (!WinActive("DaVinci Resolve - ahk_exe Resolve.exe"))
    {
        cl("Activating dv")
        WinActivate("DaVinci Resolve - ahk_exe Resolve.exe")
        Sleep 100
    }
}

runScript(action, content)
{
    focusDavinci()    
    ini("action", action)
    ini("content", content)
    Send "^{Delete}"
}

cl(text, overwrite := false) {
    if (overwrite) {
        FileDelete("log.txt")
    }
    FileAppend(text "`n", "log.txt")
}
cl(A_Now, true)