import numpy as np
import matplotlib


class MK:
    def __init__(self, data):
        self.data = data
        self.len = len(data)
        self.UF = np.zeros(self.len)         #定义统计量UF
        self.UB = np.zeros(self.len)         #定义统计量UB
        self.avg = self.len*(self.len-1)/4   #累计数s(k)的均值
        self.std = self.len * (self.len - 1) * (2 * self.len + 5) / 72 #累计数s(k)的方差
        self.r1 = []
        self.r2 = []
        def frontRank(self):
            # 定义秩序列，r(i)记录的是第i个时刻，其数值大于j时刻(其中j<=i)数值的个数的
            for i in range(self.len):
                r_sum = 0
                for j in range(0, i+1):
                    if self.data[i]>self.data[j]:
                        r_sum+=1
                self.r1.append(r_sum)
            # 定义累计量序列s，s(k)记录的是第i个时刻(其中i<=k)，其数值大于j时刻(其中j<=i)数值个数的累计数
            s = np.zeros(self.len)
            # k从2开始，因为根据统计量UF(k)公式，k=1时，s(1)、E(1)、Var(1)均为0，此时UF无意义，因此公式中，令UFk(1)=0
            for k in range(2, self.len):
                for i in range(1, k+1):
                    s[k]+=self.r1[i]
                E = k * (k - 1) / 4                     # s(k)的均值
                Var = k * (k - 1) * (2 * k + 5) / 72    # s(k)的方差
                self.UF[k] = (s[k] - E) / np.sqrt(Var)

        def backRank(self):
            self.r2 = self.r1.reverse()
            for i in range(self.len):
                r_sum = 0
                for j in range(0, i+1):
                    if self.data[i]>self.data[j]:
                        r_sum+=1
                self.r2.append(r_sum)
            s = np.zeros(self.len)
            for k in range(2, self.len):
                for i in range(1, k+1):
                    s[k]+=self.r2[i]
                E = k * (k - 1) / 4                     # s(k)的均值
                Var = k * (k - 1) * (2 * k + 5) / 72    # s(k)的方差
                self.UB[k] = -1*(s[k] - E) / np.sqrt(Var)
                self.UB = self.UB.reverse()

    def plot(self):
        pass



