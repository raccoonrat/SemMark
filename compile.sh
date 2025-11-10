#!/bin/bash
# 编译 LaTeX 文档为 PDF
# 使用 XeLaTeX 编译，支持中文

echo "正在编译 semmark.tex..."
echo ""

# 第一次编译
xelatex -interaction=nonstopmode semmark.tex

# 第二次编译（处理交叉引用）
xelatex -interaction=nonstopmode semmark.tex

echo ""
echo "编译完成！"
echo "生成的 PDF 文件: semmark.pdf"
echo ""

# 询问是否清理辅助文件
read -p "是否清理辅助文件 (y/n)? " clean
if [ "$clean" = "y" ] || [ "$clean" = "Y" ]; then
    echo "正在清理辅助文件..."
    rm -f *.aux *.log *.out *.toc *.bbl *.blg
    echo "清理完成！"
fi

