#Requires AutoHotkey v2.0

active_project := FileRead("activeproject.txt")

if (ProcessExist("Resolve.exe") and A_Args.Has(1))
{

    dest := "screenshot-" A_Now ".png"

    path := active_project "\" dest

    FileMove A_Args[1], path
    WinActivate("Davinci Resolve - ", "ahk_exe Resolve.exe")

    ; Try to run as fast as possible by looping and checking if the window is active
    Loop 20 {
        Sleep 100
        if (WinActive("ahk_exe Resolve.exe")) {
            Sleep 100
            Run '"C:\YouTube\Scripts\davinci-script.ahk" addnewclip "' path '"'
        }
        Break
    }
}