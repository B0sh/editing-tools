@echo off
setlocal

set "height=480"
set "dir=%~1"
set "ffmpeg_path=ffmpeg.exe"

if not defined dir (
    echo No directory provided. Using the current directory.
    set "dir=%cd%"
)

if not exist "%dir%" (
    echo The specified directory does not exist.
    exit /b
)

cd /d "%dir%"

dir /b *.mkv >nul 2>&1
if errorlevel 1 (
    echo No MKV files found in the specified directory.
    exit /b
)

if not exist proxies mkdir proxies

for %%F in (*.mkv) do (
    echo Processing: %%~nF
    "%ffmpeg_path%" -i "%%~nxF" -map 0 -vf "scale=-2:%height%" -c:v libx264 -crf 23 -c:a copy -y "proxies\%%~nF_%height%proxy.mkv"
)

echo Done.
endlocal
