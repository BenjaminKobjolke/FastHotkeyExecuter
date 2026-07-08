; Go to Sent — standalone action launched by FastHotkeyExecuter (run entry)
TbSleep := 100
WinActivate, ahk_exe thunderbird.exe
WinWaitActive, ahk_exe thunderbird.exe, , 2
Send, {ESC}
Sleep, %TbSleep%
Send, g
Sleep, %TbSleep%
Send, xdmain
Sleep, %TbSleep%
Send, {SPACE}
Sleep, %TbSleep%
Send, sent
Sleep, 50
Send, {Enter}
Sleep, 100
RunWait, "%A_AhkPath%" "%A_ScriptDir%\focus_results.ahk"
