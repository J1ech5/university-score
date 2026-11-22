# -*- coding: utf-8 -*-
"""
毕设项目：高校分数线数据可视化分析
功能模块：
1. 构建/读取分数线数据集
2. Pandas完成数据清洗（去重、缺失值、异常分数过滤）
3. Matplotlib生成静态趋势图
4. Pyecharts生成交互式可视化图表（ECharts）
5. 分组统计，输出各校平均分
"""
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts.charts import Line
from pyecharts import options as opts
import os

# 创建文件夹
os.makedirs("data", exist_ok=True)
os.makedirs("images", exist_ok=True)
os.makedirs("output", exist_ok=True)

# ====================== 1. 数据集构建 ======================
data = [
    ["沧州交通学院", "河北", "物联网工程", 2023, 432, 440, "本科批"],
    ["沧州交通学院", "河北", "物联网工程", 2024, 445, 451, "本科批"],
    ["沧州交通学院", "河北", "物联网工程", 2025, 453, 460, "本科批"],
    ["河北科技大学", "河北", "物联网工程", 2023, 480, 488, "本科批"],
    ["河北科技大学", "河北", "物联网工程", 2024, 492, 499, "本科批"],
    ["河北科技大学", "河北", "物联网工程", 2025, 501, 508, "本科批"],
    ["石家庄铁道大学", "河北", "计算机科学与技术", 2023, 510, 518, "本科批"],
    ["石家庄铁道大学", "河北", "计算机科学与技术", 2024, 522, 529, "本科批"],
    ["石家庄铁道大学", "河北", "计算机科学与技术", 2025, 530, 536, "本科批"],
    ["河北化工医药职业技术学院", "河北", "计算机应用技术", 2023, 380, 389, "专科批"],
    ["河北化工医药职业技术学院", "河北", "计算机应用技术", 2024, 391, 398, "专科批"],
    ["河北化工医药职业技术学院", "河北", "计算机应用技术", 2025, 402, 409, "专科批"],
]
columns = ["school", "province", "major", "year", "min_score", "avg_score", "batch"]
df = pd.DataFrame(data, columns=columns)
df.to_csv("university_score.csv", index=False, encoding="utf-8-sig")
print("✅ 数据集已生成 data/university_score.csv")

# ====================== 2. 数据清洗函数 ======================
def data_clean(df_input):
    df_clean = df_input.drop_duplicates()
    df_clean = df_clean.dropna()
    df_clean = df_clean[(df_clean["min_score"] >= 200) & (df_clean["min_score"] <= 750)]
    print("✅ 数据清洗完成，清洗后数据行数：", len(df_clean))
    return df_clean

df_cleaned = data_clean(df)

# ====================== 3. Matplotlib 静态可视化 ======================
plt.rcParams["font.sans-serif"] = ["Arial Unicode MS"]
plt.rcParams["axes.unicode_minus"] = False

iot_df = df_cleaned[df_cleaned["major"] == "物联网工程"]
pivot_iot = iot_df.pivot(index="year", columns="school", values="avg_score")
pivot_iot.plot(kind="line", marker='o')
plt.title("物联网工程专业历年平均分趋势")
plt.xlabel("年份")
plt.ylabel("平均分")
plt.savefig("images/static_trend.png", dpi=300, bbox_inches="tight")
plt.close()
print("✅ 静态折线图保存 images/static_trend.png")

# ====================== 4. Pyecharts（✅修复numpy类型转原生python类型） ======================
def interactive_line():
    line = Line(init_opts=opts.InitOpts(width="900px", height="500px"))
    # ✅ 核心修复：numpy.int → python原生int，再转字符串作为类目
    years = sorted([int(y) for y in df_cleaned["year"].unique()])
    years_str = [str(y) for y in years]
    line.add_xaxis(xaxis_data=years_str)
    for school in df_cleaned["school"].unique():
        school_data = df_cleaned[df_cleaned["school"] == school].sort_values("year")
        # ✅ 分数同样转原生int，防止变成null
        scores = [int(s) for s in school_data["avg_score"].tolist()]
        line.add_yaxis(series_name=school, y_axis=scores, markpoint_opts=opts.MarkPointOpts(data=[opts.MarkPointItem(type_="max"),opts.MarkPointItem(type_="min")]))
    line.set_global_opts(
        title_opts=opts.TitleOpts(title="多院校历年平均分交互式趋势图"),
        xaxis_opts=opts.AxisOpts(name="年份", type_="category"),
        yaxis_opts=opts.AxisOpts(name="平均分"),
        tooltip_opts=opts.TooltipOpts(trigger="axis")
    )
    line.render("output/interactive_trend.html")
    print("✅ 交互式图表保存 output/interactive_trend.html")

interactive_line()

# ====================== 5. 统计分析输出 ======================
group_school = df_cleaned.groupby("school")["avg_score"].mean().reset_index()
print("\n📊 各校近三年平均分数线：")
print(group_school)

print("\n🎉 项目运行完毕！")