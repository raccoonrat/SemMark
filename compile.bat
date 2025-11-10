@echo off
REM 编译 LaTeX 文档为 PDF
REM 使用 XeLaTeX 编译，支持中文

echo 正在编译 semmark.tex...
echo.

REM 第一次编译
xelatex -interaction=nonstopmode semmark.tex

REM 第二次编译（处理交叉引用）
xelatex -interaction=nonstopmode semmark.tex

echo.
echo 编译完成！
echo 生成的 PDF 文件: semmark.pdf
echo.

REM 询问是否清理辅助文件
set /p clean="是否清理辅助文件 (y/n)? "
if /i "%clean%"=="y" (
    echo 正在清理辅助文件...
    del *.aux *.log *.out *.toc *.bbl *.blg 2>nul
    echo 清理完成！
)

pause

