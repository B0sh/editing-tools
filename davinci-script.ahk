#Requires AutoHotkey v2.0

ini(key, value) {
    IniWrite value, "C:\YouTube\davinci.ini", "davinci", key
}

if (WinActive("ahk_exe Resolve.exe") and A_Args.Has(1))
{
    ini("action", A_Args[1])

    if (A_Args.Has(2)) {
        ini("content", A_Args[2])
    }
    else {
        ini("content", "")
    }

    Send "!{F10}"
}