#Requires AutoHotkey v2.0

ini(key, value) {
    IniWrite value, "C:\YouTube\davinci.ini", "davinci", key
}

runScript(action, content) {
    if (WinActive("ahk_exe Resolve.exe") and A_Args.Has(1))
    {
        ini("action", action)
        ini("content", A_Args[2])

        Send "!{F10}"
    }
}

if (A_Args.Has(1)) {
    if (A_Args.Has(2)) {
        runScript(A_Args[1], A_Args[2])
    }
    else {
        runScript(A_Args[1], "")
    }
}