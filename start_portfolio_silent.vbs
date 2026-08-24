Set WshShell = CreateObject("WScript.Shell")
WshShell.CurrentDirectory = "C:\Users\SHARAN\Downloads\portfolio"
WshShell.Run "python server.py", 0, False
