@echo off
REM QuantstatsWebApp Environment Management Script
REM Compatible with Windows Command Prompt

SETLOCAL ENABLEEXTENSIONS
SET VENV_DIR=venv
SET PYTHON_EXE=python
SET REQUIREMENTS=requirements.txt
SET PYPROJECT=pyproject.toml

:mainmenu
cls
ECHO =============================================
ECHO QuantstatsWebApp Environment Management
ECHO =============================================
ECHO 1. Create virtual environment (Python 3.10.11)
ECHO 2. Activate virtual environment
ECHO 3. Install dependencies (uv)
ECHO 4. Install dependencies (pip)
ECHO 5. Run Flask app
ECHO 6. Run unit tests
ECHO 7. Update requirements.txt from pyproject.toml
ECHO 8. Exit
ECHO =============================================
SET /P CHOICE=Select an option (1-8): 

IF "%CHOICE%"=="1" GOTO createvenv
IF "%CHOICE%"=="2" GOTO activatevenv
IF "%CHOICE%"=="3" GOTO installuv
IF "%CHOICE%"=="4" GOTO installpip
IF "%CHOICE%"=="5" GOTO runapp
IF "%CHOICE%"=="6" GOTO runtests
IF "%CHOICE%"=="7" GOTO update_requirements
IF "%CHOICE%"=="8" GOTO end
GOTO mainmenu

:createvenv
ECHO Creating virtual environment with Python 3.10.11...
%PYTHON_EXE% -m venv %VENV_DIR%
ECHO Done.
PAUSE
GOTO mainmenu

:activatevenv
ECHO To activate the virtual environment, run:
ECHO %VENV_DIR%\Scripts\activate
PAUSE
GOTO mainmenu

:installuv
ECHO Installing dependencies using uv...
CALL %VENV_DIR%\Scripts\activate && pip install uv && uv pip install --all --upgrade --refresh
PAUSE
GOTO mainmenu

:installpip
ECHO Installing dependencies using pip...
CALL %VENV_DIR%\Scripts\activate && pip install -r %REQUIREMENTS%
PAUSE
GOTO mainmenu

:runapp
ECHO Running Flask app...
CALL %VENV_DIR%\Scripts\activate && set FLASK_APP=app.py && flask run
PAUSE
GOTO mainmenu

:runtests
ECHO Running unit tests...
CALL %VENV_DIR%\Scripts\activate && python -m unittest discover tests
PAUSE
GOTO mainmenu

:update_requirements
ECHO Updating requirements.txt from pyproject.toml...
CALL %VENV_DIR%\Scripts\activate && pip install toml && python -c "import toml; py = toml.load('%PYPROJECT%'); deps = py['project']['dependencies']; open('%REQUIREMENTS%', 'w').write('\n'.join(['# Project dependencies for QuantstatsWebApp'] + deps))"
ECHO requirements.txt updated.
PAUSE
GOTO mainmenu

:end
ECHO Exiting...
ENDLOCAL
EXIT /B 0
