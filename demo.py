import pandas as pd
import numpy as np

# 读取CSV文件
df = pd.read_csv('scope_0.csv')  # 替换'your_file.csv'为你的CSV文件路径

# 假设我们有一个名为'string_column'的列，其中包含可以转换为数字的字符串
# 使用astype方法将字符串列转换为浮点数（或整数，如果需要）
df['sec'] = pd.to_numeric(df['sec'], errors='raise')
df['Volt1'] = pd.to_numeric(df['Volt1'], errors='raise')

# 'errors'参数设置为'coerce'会将无法转换的值设置为NaN（不是一个数字）
# 如果你确定所有字符串都可以转换为数字，可以将'errors'设置为'raise'来让pandas在遇到无法转换的值时抛出异常

# print(df)


def find_edges(data, low_threshold):
    #
    up_edges = data[(df['slope'] > low_threshold)
                    | ((df['slope'] > (low_threshold / 2))
                       & (df['slope'].shift(1) > (low_threshold / 2)))]
    return up_edges


def compute_slope(values):
    # 计算斜率
    x = [0, 1]
    y = values

    # return 0
    # 使用NumPy的polyfit来拟合一阶多项式并获取斜率
    slope, intercept = np.polyfit(x, y, 1)
    return slope


window_size = 2  # 设置滑动窗口的大小
slope = df['Volt1'].rolling(window=window_size).apply(compute_slope, raw=True)

df['slope'] = slope
df['slope'] = df['slope'].abs()

# print(df)
df.to_csv('temp.csv')
edges = find_edges(df, 2)
print(edges.count())
edges.to_csv('result.csv')
