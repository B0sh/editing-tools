#Requires AutoHotkey v2.0

active_project := "C:\YouTube\Minecraft\3-13-23 password"

if (ProcessExist("Resolve.exe") and A_Args.Has(1))
{

    dest := "screenshot-" A_Now ".png"

    path := active_project "\" dest

    FileMove A_Args[1], path
    WinActivate "ahk_exe Resolve.exe"

    ; Try to run as fast as possible by looping and checking if the window is active
    Loop 20 {
        if (WinActive("ahk_exe Resolve.exe")) {
            Run '"C:\YouTube\Scripts\davinci-script.ahk" addnewclip "' path '"'
        }
        Sleep 100
        Break
    }
}