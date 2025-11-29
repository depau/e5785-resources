@title Modem Unlock V7R22

@setlocal

@prompt $G

@if not exist bin\adb.exe (
  echo.
  echo Attention, not all necessary files are present for operation - you may not have unpacked the archive completely!
  goto quit
)

@echo.
@echo IP address of the modem:
@echo 1 or Enter - 192.168.8.1
@echo 2           - 192.168.1.1
@echo 3           - other
@echo 0           - exit
@set choice=1
@set /P choice=": "

@if "%choice%" == "0" goto :eof

@^\
if not "%choice%" == "1" (
if not "%choice%" == "2" (
if not "%choice%" == "3" (
  echo.
  echo Invalid choice
  goto quit
)))

@if "%choice%" == "1" set ip_addr=192.168.8.1
@if "%choice%" == "2" set ip_addr=192.168.1.1

@if not "%choice%" == "3" goto l1

@echo.
@set ip_addr=
@set /P ip_addr="Enter IP address: "

@if not defined ip_addr (
  echo.
  echo Invalid input
  goto quit
)

:l1

@bin\adb kill-server

bin\adb connect %ip_addr%:5555

bin\adb push bin\balong-nvtool /

bin\adb shell chmod 777 /balong-nvtool

bin\adb shell /balong-nvtool -m 8268:01:00:00:00:02:00:00:00:0A:00:00:00

bin\adb shell rm /balong-nvtool

@echo.
@echo Rebooting the modem...

bin\adb shell "echo -en 'AT^RESET\r' > /dev/appvcom1"

@bin\adb kill-server

:quit

@echo.
@echo The script has finished. Press any key
@pause > nul

@exit /B⏎
