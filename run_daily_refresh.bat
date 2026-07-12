@echo off

cd /d C:\Users\DELL\Desktop\OTT-Trend-Intelligence

call .venv\Scripts\activate.bat

python src\automation\daily_refresh.py

