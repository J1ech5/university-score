# 高校分数线数据可视化分析

## 项目简介
本项目使用 Python 完成河北省多所高校分数线的数据处理与可视化。
对物联网工程、计算机相关专业近几年录取分数线做清洗、统计，生成静态图和交互式图表，直观展示分数变化趋势。

## 使用技术
- Python
- Pandas：数据清洗、表格处理
- Matplotlib：生成静态折线图
- Pyecharts：制作可交互网页图表

## 文件说明
- `main.py`：主程序，运行后生成数据集和图表
- `requirements.txt`：需要安装的第三方库
- `data/`：存放分数线 csv 数据文件
- `images/`：保存静态图片
- `output/`：保存交互式 html 图表
- `README.md`：项目说明文档

## 运行方法
1. 安装依赖包
```bash
pip install -r requirements.txt
