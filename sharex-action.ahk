#Requires AutoHotkey v2.0
#Include davinci-shared.ahk

active_project := FileRead("activeproject.txt")
if (A_Args.Has(1))
{
    focusDavinci()
    Sleep 300

    dest := "screenshot-" A_Now ".png"
    path := active_project "\" dest
    FileMove A_Args[1], path

    try
    {
        if (ImageSearch(&FoundX, &FoundY, 0, 0, A_ScreenWidth, A_ScreenHeight, "images/resolve-master.png"))
        {
            MouseGetPos &xpos, &ypos
            Click FoundX + 50, FoundY + 10
            Sleep 100
            MouseMove xpos, ypos
        }
    }
    catch as exc
    {
        MsgBox "Could not conduct the search due to the following error:`n" exc.Message
    } 

    runScript("addnewclip", path)
}