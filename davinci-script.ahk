#Requires AutoHotkey v2.0
#Include davinci-shared.ahk

if (!ProcessExist("Resolve.exe")) {
    Return
}

if (A_Args.Has(1)) {
    if (A_Args.Has(2)) {
        runScript(A_Args[1], A_Args[2])
    }
    else {
        runScript(A_Args[1], "")
    }
}