@echo off
setlocal

REM Check if ruamel.yaml is installed
python -c "import ruamel.yaml" 2>nul

if %errorlevel% neq 0 (
    REM If ruamel.yaml is not installed, show prompt
    echo msgbox "ruamel.yaml is not installed. Do you want to install it?", vbYesNo + vbQuestion, "Install ruamel.yaml?" > "%temp%\confirm.vbs"
    cscript /nologo "%temp%\confirm.vbs" >nul
    if %errorlevel% neq 6 (
        REM If the user closes the prompt, exit the script
        echo Installation cancelled.
        exit /b
    )

    REM User confirmed, attempt to install ruamel.yaml
    echo Installing ruamel.yaml...
    pip install ruamel.yaml
    if %errorlevel% neq 0 (
        REM If the first attempt fails, try the Tsinghua mirror
        echo Failed to install using default index. Trying Tsinghua mirror...
        pip install ruamel-yaml -i https://pypi.tuna.tsinghua.edu.cn/simple
        if %errorlevel% neq 0 (
            REM If installation fails, exit the script
            echo Failed to install ruamel.yaml. Exiting.
            exit /b
        )
    )
)

REM ruamel.yaml is installed, running AutoPFX
echo Running AutoPFX...
python AutoPFX.py

endlocal
