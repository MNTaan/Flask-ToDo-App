Set WshShell = CreateObject("WScript.Shell")
' Chạy file app.py ngầm bằng pythonw (không hiện bất kỳ cửa sổ CMD/PowerShell nào)
WshShell.CurrentDirectory = CreateObject("Scripting.FileSystemObject").GetParentFolderName(WScript.ScriptFullName)
WshShell.Run "pythonw app.py", 0, False
