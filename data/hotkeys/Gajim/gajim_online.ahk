; Save current window state and resize to recorded dimensions
_targetHwnd := WinExist("A")
WinGetPos, _origX, _origY, _origW, _origH, ahk_id %_targetHwnd%
WinMove, ahk_id %_targetHwnd%, , %_origX%, %_origY%, 1293, 1082
Sleep, 300

Loop, 1
{

SetTitleMatchMode, 2
CoordMode, Mouse, Window

Sleep, 586

MouseClick, L, 41, 1015

Sleep, 492

MouseClick, L, 876, 449

Sleep, 539

MouseClick, L, 894, 257

Sleep, 765

MouseClick, L, 41, 147

Sleep, 1000

}

; Restore original window state
WinMove, ahk_id %_targetHwnd%, , %_origX%, %_origY%, %_origW%, %_origH%
