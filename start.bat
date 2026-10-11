@echo off
chcp 65001 >nul
title RAG系统启动器

echo ============================================
echo  RAG 智能知识问答系统 - 一键启动
echo ============================================
echo.

cd /d "%~dp0"

echo [1/2] 正在启动后端 (端口 8080)...
start "RAG后端(8080)" python -m uvicorn backend.routes.app_routes:app --host 0.0.0.0 --port 8080

echo [2/2] 正在启动前端 (端口 3000)...
cd /d "%~dp0domain"
start "RAG前端(3000)" python -m http.server 3000

echo.
echo 启动完成！请稍候片刻，然后浏览器访问：
echo     http://localhost:3000
echo.
echo 关闭窗口不会停止服务；如需停止，请在对应窗口按 Ctrl+C。
echo.
pause