@echo off
REM ==================================
REM = Batch script for imageexporter =
REM ==================================

set /p id="What drive-letter does the USB have? " %=%
set usb_drive=%id%:\

copy C:\Bildspel\bildspel.py "C:\Documents and Settings\Bibblan\My Documents\My Pictures"
cd "C:\Documents and Settings\Bibblan\My Documents\My Pictures"
python bildspel.py -p kamera -e %usb_drive%
python bildspelpy -p "inscannade bilder" -e %usb_drive%
