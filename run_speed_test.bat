@echo off
setlocal

rem Вставьте прямую ссылку на картинку между кавычками после знака равенства.
set "URL=https://www.zastavki.com/pictures/originals/2024/Nature___Mountains_View_of_a_mountain_peak_near_a_lake_168306_.jpg"

if "%URL%"=="" (
    echo Сначала откройте этот BAT через Изменить и укажите прямой URL картинки в строке URL.
    echo Пример: set "URL=https://example.com/large-image.jpg"
    pause
    exit /b 1
)

py "%~dp0speed_test.py" "%URL%"
if errorlevel 1 (
    echo.
    echo Тест завершился с ошибкой.
    pause
    exit /b 1
)

pause
