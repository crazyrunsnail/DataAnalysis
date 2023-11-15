from tokenize import group
import pandas as pd
import numpy as np


cols = ["name", "sex", "births"]

years = range(1880, 2023)

frames = []
for year in years:
    frame = pd.read_csv(f"datasets/names/yob{year}.txt", names=cols)
    frame["year"] = year
    frames.append(frame)

data = pd.concat(frames, ignore_index=True)

# print(f"len of data : {len(data)}")


# 计算男女比例在
#   grouped_data = data.groupby(["year", "sex"]).size().unstack("sex")
#   grouped_data["diff"] = grouped_data["F"] - grouped_data["M"]
#   grouped_data["m_prop"] = round(
#       grouped_data["M"] / (grouped_data["F"] + grouped_data["M"]), 2
#   )
# 这是另外一种计算方法
# pivoted = grouped_data.pivot(index="year", columns="sex", values="births").reset_index()
# pivoted['male_prop'] = pivoted['M'] / (pivoted['M'] + pivoted['F'])


def add_prop(grouped):
    grouped["prop"] = grouped.births / grouped.births.sum()
    return grouped


# 计算当前名称人数/当年性别人数
grouped_data = data.groupby(["year", "sex"], group_keys=False).apply(add_prop)
print(grouped_data[:100])

# print(
#     grouped_data.groupby(["year", "sex"], group_keys=False).births.sum()
# )  # 7065 201484


top1000 = grouped_data.groupby(["year", "sex"], group_keys=False).apply(
    lambda grouped: grouped.sort_values(by=["births"], ascending=False)[:1000]
)

print(len(top1000))

name_births = top1000.pivot_table(
    values="births", index="year", columns="name", aggfunc=sum
)


name_births[["John", "Harry", "Mary", "Marilyn"]].plot(
    title="Number of births per year", subplots=True, figsize=(12, 10), grid=False
)


# 计算前1000的占比
table = top1000.pivot_table(values="prop", index="year", columns="sex", aggfunc=sum)

# 查找类加和0.5的数量
print(
    top1000.loc[top1000.year == 2010]
    .loc[top1000.sex == "M"]
    .sort_values(by="prop", ascending=False)
    .prop.cumsum()
    .values.searchsorted(0.5)
)
