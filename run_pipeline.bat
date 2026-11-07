@echo off
cd /d %~dp0
if not exist logs mkdir logs
call .venv\Scripts\activate.bat

echo [%date% %time%] pipeline start >> logs\pipeline.log

python ingest\ingest.py >> logs\pipeline.log 2>&1
if errorlevel 1 goto fail

dbt run --profiles-dir . >> logs\pipeline.log 2>&1
if errorlevel 1 goto fail

dbt test --profiles-dir . >> logs\pipeline.log 2>&1
if errorlevel 1 goto fail

echo [%date% %time%] pipeline OK >> logs\pipeline.log
exit /b 0

:fail
echo [%date% %time%] pipeline FAILED >> logs\pipeline.log
exit /b 1