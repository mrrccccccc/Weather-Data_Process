import numpy as np
import matplotlib.pyplot as plt


class MK:
    def __init__(self, data):
        self.data = data
        self.len = len(data)
        self.UF = frontRank(data=self.data)  # 定义统计量UF
        self.UB = backRank(data=self.data)

    def plot(self):
        start = 2021-self.len+1
        x = [i for i in range(start, 2022)]
        plt.plot(x, self.UF, label="UF")
        plt.plot(x, self.UB, label="UB")
        plt.plot(x, 1.96 * np.ones(self.len), '-.r', 1)
        plt.plot(x, -1.96 * np.ones(self.len), '-.r', 1)
        plt.plot(x, 0 * np.ones(self.len), '-.r', 1)
        plt.legend()
        plt.axis([start, 2021, -5, 5])
        plt.show()


# 定义秩序列，r(i)记录的是第i个时刻，其数值大于j时刻(其中j<=i)数值的个数的
def frontRank(data):
    UF = np.zeros(len(data))  # 定义统计量UF
    r1 = []
    for i in range(len(data)):
        r_sum = 0
        for j in range(0, i + 1):
            if data[i] > data[j]:
                r_sum += 1
        r1.append(r_sum)
    # 定义累计量序列s，s(k)记录的是第i个时刻(其中i<=k)，其数值大于j时刻(其中j<=i)数值个数的累计数
    s = np.zeros(len(data))
    # k从2开始，因为根据统计量UF(k)公式，k=1时，s(1)、E(1)、Var(1)均为0，此时UF无意义，因此公式中，令UFk(1)=0
    for k in range(2, len(data)):
        for i in range(1, k + 1):
            s[k] += r1[i]
        E = k * (k - 1) / 4  # s(k)的均值
        Var = k * (k - 1) * (2 * k + 5) / 72  # s(k)的方差
        UF[k] = (s[k] - E) / np.sqrt(Var)
    return UF


def backRank(data):
    UB = np.zeros(len(data))
    r2 = []
    data.reverse()
    for i in range(len(data)):
        r_sum = 0
        for j in range(0, i + 1):
            if data[i] > data[j]:
                r_sum += 1
        r2.append(r_sum)
    s = np.zeros(len(data))
    for k in range(2, len(data)):
        for i in range(1, k + 1):
            s[k] += r2[i]
        E = k * (k - 1) / 4  # s(k)的均值
        Var = k * (k - 1) * (2 * k + 5) / 72  # s(k)的方差
        UB[k] = -1 * (s[k] - E) / np.sqrt(Var)
    UB2 = []
    for i in range(len(data)):
        UB2.append(UB[len(data)-i-1])
    return UB2

