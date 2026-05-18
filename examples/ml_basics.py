"""
机器学习入门经典代码示例
========================
涵盖三大类型：监督学习、无监督学习、简单神经网络
依赖：pip install scikit-learn numpy matplotlib
"""

import numpy as np
from sklearn.datasets import load_iris, make_classification, make_regression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import accuracy_score, mean_squared_error
import warnings
warnings.filterwarnings('ignore')

# ============================================================
# 示例 1：监督学习 —— 分类（使用鸢尾花数据集）
# ============================================================
print("=" * 60)
print("📊 示例 1：分类 —— 预测鸢尾花种类")
print("=" * 60)

# 加载经典数据集：鸢尾花（3类，4个特征）
iris = load_iris()
X, y = iris.data, iris.target

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"数据集大小：{X.shape[0]} 个样本，{X.shape[1]} 个特征")
print(f"类别：{iris.target_names}")
print(f"特征：{iris.feature_names}")
print(f"训练集：{X_train.shape[0]} 个，测试集：{X_test.shape[0]} 个")

# 使用 K 近邻算法（KNN）
knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(X_train, y_train)

y_pred = knn.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"\n✅ KNN 分类准确率：{acc:.2f} ({acc*100:.1f}%)")

# 再看决策树
dt = DecisionTreeClassifier(max_depth=3, random_state=42)
dt.fit(X_train, y_train)
y_pred_dt = dt.predict(X_test)
acc_dt = accuracy_score(y_test, y_pred_dt)
print(f"✅ 决策树分类准确率：{acc_dt:.2f} ({acc_dt*100:.1f}%)")

# 预测一个新样本（自己构造一朵花）
new_flower = np.array([[5.1, 3.5, 1.4, 0.2]])  # 花萼长、宽，花瓣长、宽
pred_class = knn.predict(new_flower)[0]
print(f"\n🌺 新样本预测：这是一朵 {iris.target_names[pred_class]}")


# ============================================================
# 示例 2：监督学习 —— 回归（房价预测）
# ============================================================
print("\n" + "=" * 60)
print("💰 示例 2：回归 —— 房价预测")
print("=" * 60)

# 生成模拟房价数据
# 特征：面积（平米）、卧室数量、距市中心距离（km）
np.random.seed(42)
n_samples = 200
area = np.random.normal(100, 30, n_samples)           # 面积
bedrooms = np.random.randint(1, 5, n_samples)          # 卧室数
distance = np.random.uniform(0.5, 20, n_samples)       # 距市中心距离

# 构造房价：真实世界的大致规律
price = (
    50 +                        # 基础价（万）
    area * 0.8 +                # 面积贡献
    bedrooms * 15 +             # 卧室数贡献
    -distance * 3 +             # 距市中心越远越便宜
    np.random.normal(0, 10, n_samples)  # 随机噪声
)

X_house = np.column_stack([area, bedrooms, distance])
y_price = price

# 划分数据集
Xh_train, Xh_test, yh_train, yh_test = train_test_split(
    X_house, y_price, test_size=0.2, random_state=42
)

# 训练线性回归模型
lr = LinearRegression()
lr.fit(Xh_train, yh_train)

yh_pred = lr.predict(Xh_test)
mse = mean_squared_error(yh_test, yh_pred)
rmse = np.sqrt(mse)

print(f"训练样本数：{Xh_train.shape[0]}，测试样本数：{Xh_test.shape[0]}")
print(f"模型系数：")
print(f"  截距（基础价）：{lr.intercept_:.1f} 万")
print(f"  面积系数：{lr.coef_[0]:.2f} 万/平米")
print(f"  卧室数系数：{lr.coef_[1]:.2f} 万/间")
print(f"  距市中心系数：{lr.coef_[2]:.2f} 万/km")
print(f"\n✅ 预测误差（RMSE）：{rmse:.1f} 万")
print(f"  平均房价：{yh_test.mean():.1f} 万，误差占比约 {rmse/yh_test.mean()*100:.1f}%")

# 预测一套新房
new_house = np.array([[120, 3, 5]])  # 120平，3室，距市中心5km
pred_price = lr.predict(new_house)[0]
print(f"\n🏠 新房子预测：120平/3室/距市中心5km → 约 {pred_price:.0f} 万元")


# ============================================================
# 示例 3：无监督学习 —— 聚类（客户分群）
# ============================================================
print("\n" + "=" * 60)
print("👥 示例 3：聚类 —— 客户分群（K-Means）")
print("=" * 60)

# 生成模拟客户数据（消费金额、购买频率）
np.random.seed(42)
n_customers = 300

# 三类客户：高消费低频、中消费中频、低消费高频
cluster1 = np.random.multivariate_normal([5000, 2],  [[800, 0], [0, 0.5]], 100)
cluster2 = np.random.multivariate_normal([2000, 8],  [[400, 0], [0, 1.0]], 100)
cluster3 = np.random.multivariate_normal([300, 20],  [[100, 0], [0, 3.0]], 100)

customers = np.vstack([cluster1, cluster2, cluster3])

# 用 K-Means 自动分成 3 类
kmeans = KMeans(n_clusters=3, random_state=42, n_init=10)
labels = kmeans.fit_predict(customers)

print("模型自动发现的 3 个客户群体：")
for i in range(3):
    mask = labels == i
    avg_spend = customers[mask, 0].mean()
    avg_freq = customers[mask, 1].mean()
    print(f"  群组 {i+1}：平均消费 {avg_spend:.0f} 元，平均购买频率 {avg_freq:.1f} 次/月")


# ============================================================
# 示例 4：动手搭建一个简单的神经网络（用 NumPy）
# ============================================================
print("\n" + "=" * 60)
print("🧠 示例 4：从零搭建一个神经元（感知机）")
print("=" * 60)

def sigmoid(x):
    """Sigmoid 激活函数"""
    return 1 / (1 + np.exp(-np.clip(x, -500, 500)))

def neuron_forward(weights, bias, inputs):
    """一个神经元的前向传播"""
    z = np.dot(weights, inputs) + bias
    return sigmoid(z)

# 训练一个简单的 AND 门
print("训练一个 AND 逻辑门：")
print("  x1  x2 | y")
print("  --------|----")

X_and = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
y_and = np.array([0, 0, 0, 1])  # AND 真值表

# 手动训练（可以用梯度下降，这里直接展示训练后的权重）
w = np.array([10.0, 10.0])  # 训练好的权重
b = -15.0                   # 训练好的偏置

for i, x in enumerate(X_and):
    pred = neuron_forward(w, b, x)
    print(f"  {x[0]}   {x[1]}  | {pred:.4f}  (四舍五入: {int(round(pred))})")

print(f"\n✅ 预测结果与 AND 逻辑一致！")
print(f"  权重：w1={w[0]}, w2={w[1]}, 偏置：b={b}")
print(f"  逻辑公式：输出 = sigmoid(10*x1 + 10*x2 - 15)")
print(f"  只有当 x1=1 且 x2=1 时，结果才接近 1")


# ============================================================
# 总结
# ============================================================
print("\n" + "=" * 60)
print("📝 总结")
print("=" * 60)
print("""
机器学习就是让计算机从数据中自动学习规律：

┌─────────────────────────────────────────────┐
│  传统编程:  数据 + 规则 → 答案              │
│  机器学习:  数据 + 答案 → 规则              │
└─────────────────────────────────────────────┘

你刚才看到了：
  1️⃣ KNN 分类   —— 根据邻居的标签判断类别
  2️⃣ 线性回归   —— 用一条线拟合数据趋势
  3️⃣ K-Means    —— 自动把数据分成几群
  4️⃣ 感知机     —— 神经网络的最小单元

试试运行这个文件看看效果：
  $ python3 examples/ml_basics.py
""")
