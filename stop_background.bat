@echo off
chcp 65001 >nul
echo Dang dung tien trinh To-Do App chay ngam...
taskkill /F /IM pythonw.exe 2>nul
if %ERRORLEVEL% equ 0 (
    echo [OK] Da dung ung dung thanh cong!
) else (
    echo [INFO] Khong tim thay tien trinh dang chay hoac da duoc dung truoc do.
)
timeout /t 3
