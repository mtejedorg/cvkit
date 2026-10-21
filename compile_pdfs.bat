@echo off
REM CV Builder PDF Compiler Launcher
REM Calls the PowerShell interactive UI script

setlocal enabledelayedexpansion

REM Get the directory where this batch file is located
set "SCRIPT_DIR=%~dp0"

REM Launch the PowerShell script
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%SCRIPT_DIR%compile_pdfs.ps1"

endlocal
