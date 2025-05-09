@echo off

REM windows batch file

REM set program and rom directories here 
set ZESARUX_DIR=C:\tools\ZEsarUX_windows-12.0
set JETPAC_TZX=C:\tools\roms\Jetpac.tzx\Jetpac.tzx

rem there really should be no need to change anything below... 

rem store the current working directory
set STARTING_DIR=%CD%

REM this will run jetpac on emulator with the the remote debugging options enabled
cd %ZESARUX_DIR%
zesarux.exe --enable-remoteprotocol --tape %JETPAC_TZX%
cd %STARTING_DIR%