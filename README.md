# 大模型文本语义水印研究综述

本文档将 `semmark.md` 转换为符合 USENIX SOUPS 2020 格式的 LaTeX 论文。

## 编译说明

### 前提条件

1. **安装 LaTeX 发行版**：
   - Windows: [MiKTeX](https://miktex.org/) 或 [TeX Live](https://www.tug.org/texlive/)
   - macOS: [MacTeX](https://www.tug.org/mactex/)
   - Linux: `sudo apt-get install texlive-full` (或相应发行版的包管理器)

2. **安装中文字体支持**（如果需要）：
   - 确保系统已安装中文字体（如 SimSun, SimHei 等）
   - 或者修改 `semmark.tex` 中的字体设置

### 编译步骤

由于文档包含中文内容，需要使用 **XeLaTeX** 进行编译：

```bash
# 方法1: 使用 xelatex 命令
xelatex semmark.tex
xelatex semmark.tex  # 需要编译两次以正确处理交叉引用

# 方法2: 使用 latexmk（推荐）
latexmk -xelatex semmark.tex
```

### 编译选项

如果需要清理中间文件：

```bash
latexmk -c semmark.tex  # 清理辅助文件
latexmk -C semmark.tex  # 清理所有生成文件（包括PDF）
```

## 文件说明

- `semmark.tex`: 主 LaTeX 文档
- `semmark.md`: 原始 Markdown 文档
- `usenix2020_SOUPS.sty`: USENIX SOUPS 2020 样式文件
- `README.md`: 本说明文件

## 注意事项

1. **字体设置**：如果系统没有默认的中文字体，可能需要修改 `semmark.tex` 中的字体设置，或者安装相应的字体。

2. **编译引擎**：必须使用 XeLaTeX 编译，因为文档包含中文内容。

3. **参考文献**：参考文献使用手动管理的 `thebibliography` 环境，可以根据需要添加更多引用。

4. **表格格式**：表格使用 `table*` 环境以在双栏格式中跨栏显示。

## 内容概述

论文包含以下主要部分：

1. **引言**：介绍研究背景和范围
2. **Top30核心论文**：按主题分组介绍核心论文
3. **数据/理论差异**：关键指标波动>15%的争议点
4. **方法论分歧**：不同方法之间的对比分析
5. **矛盾点总结表**：系统梳理主要争议点
6. **引用排序**：必引Top10论文
7. **可操作建议**：基于研究侧重的具体建议
8. **结论**：总结和未来工作方向

## 修改建议

如果需要修改论文内容：

1. 编辑 `semmark.tex` 文件
2. 重新编译生成 PDF
3. 检查格式和内容是否符合要求

## 问题反馈

如果遇到编译问题，请检查：

1. LaTeX 发行版是否正确安装
2. 必要的 LaTeX 包是否已安装
3. 中文字体是否可用
4. 是否使用 XeLaTeX 编译

