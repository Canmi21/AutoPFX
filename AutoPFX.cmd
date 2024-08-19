::[Bat To Exe Converter]
::
::YAwzoRdxOk+EWAnk
::fBw5plQjdG8=
::YAwzuBVtJxjWCl3EqQJgSA==
::ZR4luwNxJguZRRnk
::Yhs/ulQjdF+5
::cxAkpRVqdFKZSTk=
::cBs/ulQjdF+5
::ZR41oxFsdFKZSTk=
::eBoioBt6dFKZSDk=
::cRo6pxp7LAbNWATEpCI=
::egkzugNsPRvcWATEpCI=
::dAsiuh18IRvcCxnZtBJQ
::cRYluBh/LU+EWAnk
::YxY4rhs+aU+IeA==
::cxY6rQJ7JhzQF1fEqQJhZkk0
::ZQ05rAF9IBncCkqN+0xwdVsFAlbi
::ZQ05rAF9IAHYFVzEqQIRPQ9bfCK6XA==
::eg0/rx1wNQPfEVWB+kM9LVsJDCWXKGSKII18
::fBEirQZwNQPfEVWB+kM9LVsJDCWXKGSKII18
::cRolqwZ3JBvQF1fEqQI4PA9EX17Nc2yzEr0J6qb44OfIgUwTWettKcD6z6CBEMYrig==
::dhA7uBVwLU+EWHqF+k85eko0
::YQ03rBFzNR3SWATEpCI=
::dhAmsQZ3MwfNWATE10M+JRIUbFbSbj/a
::ZQ0/vhVqMQ3MEVWAtB9weFUGLA==
::Zg8zqx1/OA3MEVWAtB9weVUFLA==
::dhA7pRFwIByZRRmM4FYgO0EbAwOLKGOvBPsf5+W0zOuJr0RPBa0ebZvU6pK2QA==
::Zh4grVQjdDaDJGqF4kc0ZStGQw6HP3+GJ6AI59jd19amt1kSZMQHNqrj/9Q=
::YB416Ek+ZG8=
::
::
::978f952a14a936cc963da21a135fa983
@echo off
setlocal

REM 检�?ruamel.yaml
python -c "import ruamel.yaml" 2>nul

if %errorlevel% neq 0 (
    REM 如果没有安装 ruamel.yaml
    echo msgbox "ruamel.yaml is not installed. Do you want to install it?", vbYesNo + vbQuestion, "Install ruamel.yaml?" > "%temp%\confirm.vbs"
    cscript /nologo "%temp%\confirm.vbs" >nul
    if %errorlevel% neq 6 (
        REM 用户关闭，退出脚�?
        echo Installation cancelled.
        exit /b
    )

    REM 用户确认，尝试安�?ruamel.yaml
    echo Installing ruamel.yaml...
    pip install ruamel.yaml
    if %errorlevel% neq 0 (
        REM 尝试第二个源
        echo Failed to install using default index. Trying Tsinghua mirror...
        pip install ruamel-yaml -i https://pypi.tuna.tsinghua.edu.cn/simple
        if %errorlevel% neq 0 (
            REM 退出脚�?
            echo Failed to install ruamel.yaml. Exiting.
            exit /b
        )
    )
)

REM ruamel.yaml 已经安装，运�?AutoPFX
echo Running AutoPFX...
python AutoPFX.py

endlocal
