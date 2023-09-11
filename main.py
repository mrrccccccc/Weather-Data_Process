import numpy as np
import pandas as pd


class DataProc:
    def __init__(self, file, sheet):
        self.sheet = sheet
        self.file = file
        self.listName = '20-20时降水量(毫米)'
        self.monthName = '月(月)'
        self.yearName = '年(年)'
        self.X8, self.y8= self.read('8')
        self.X9, self.y9 = self.read('9')
        self.X6, self.y6 = self.read('6')
        self.X7, self.y7 = self.read('7')
        self.X5, self.y5 = self.read('5')
        self.R8 = standardize_data(self.X8)
        self.R9 = standardize_data(self.X9)
        self.R6 = standardize_data(self.X6)
        self.R7 = standardize_data(self.X7)
        self.R5 = standardize_data(self.X5)
        self.X56 = [self.X5 + self.X6]
        self.X78 = [self.X7 + self.X8]
        self.R56 = []
        self.R78 = []
        for r1,r2 in zip(self.R5,self.R6):
            self.R56.append((r1+r2)/2)
        for r1,r2 in zip(self.R7,self.R8):
            self.R78.append((r1+r2)/2)
        self.LDFAI = cal_LDFAI(self.R56, self.R78)
        self.SDFAI56 = cal_SDFAI(self.R5, self.R6)
        self.SDFAI67 = cal_SDFAI(self.R6, self.R7)
        self.SDFAI78 = cal_SDFAI(self.R7, self.R8)
        self.SDFAI89 = cal_SDFAI(self.R8, self.R9)
        self.Z5 = cal_Z(self.R5)
        self.Z6 = cal_Z(self.R6)
        self.Z7 = cal_Z(self.R7)
        self.Z8 = cal_Z(self.R8)
        self.Z9 = cal_Z(self.R9)

    def read(self, month):
        data = pd.read_excel(io=self.file, sheet_name=self.sheet, keep_default_na=False, dtype=str, engine='openpyxl')
        data = data[data[self.monthName] == month]
        value = data[self.listName]
        year = data[self.yearName]
        df = []
        yr = []
        for i,j in zip(value,year):
            df.append(float(i))
            yr.append(float(j))
        return df,yr

    def write(self):
        writer = pd.ExcelWriter(self.sheet+'输出数据.xlsx')
        df5 = pd.DataFrame({'年份': self.y5, '标准化': self.R5,'Z': self.Z5})
        df6 = pd.DataFrame({'年份': self.y6,'标准化': self.R6,'Z': self.Z6})
        df7 = pd.DataFrame({'年份': self.y7,'标准化': self.R7,'Z': self.Z7})
        df8 = pd.DataFrame({'年份': self.y8,'标准化': self.R8,'Z': self.Z8})
        df9 = pd.DataFrame({'年份': self.y9,'标准化': self.R9,'Z': self.Z9})
        dfSDFAI56 = pd.DataFrame({'年份': self.y5,'SDFAI56': self.SDFAI56})
        dfSDFAI67 = pd.DataFrame({'年份': self.y6,'SDFAI67': self.SDFAI56})
        dfSDFAI78 = pd.DataFrame({'年份': self.y7,'SDFAI78': self.SDFAI78})
        dfSDFAI89 = pd.DataFrame({'年份': self.y8,'SDFAI89': self.SDFAI89})
        dfLDFAI = pd.DataFrame({'年份': self.y5, 'LDFAI':self.LDFAI})
        df5.index.name = '5'
        df6.index.name = '6'
        df7.index.name = '7'
        df8.index.name = '8'
        df9.index.name = '9'
        df5.to_excel(writer, sheet_name='5')
        df6.to_excel(writer, sheet_name='6')
        df7.to_excel(writer, sheet_name='7')
        df8.to_excel(writer, sheet_name='8')
        df9.to_excel(writer, sheet_name='9')
        dfSDFAI56.to_excel(writer, sheet_name='SDFAI56')
        dfSDFAI67.to_excel(writer, sheet_name='SDFAI67')
        dfSDFAI78.to_excel(writer, sheet_name='SDFAI78')
        dfSDFAI89.to_excel(writer, sheet_name='SDFAI89')
        dfLDFAI.to_excel(writer, sheet_name='LDFAI')
        writer.close()


# 降雨量的标准化处理
def standardize_data(X):
    avg_x = np.mean(X)
    std_x = np.std(X)
    R = []
    for x in X:
        r = (x - avg_x) / std_x
        R.append(r)
    return R


# LDFAI
def cal_LDFAI(R56, R78):
    LDFAI = []
    for r1, r2 in zip(R56, R78):
        ldfai = (r2 - r1) * (np.absolute(r1) + np.absolute(r2)) * np.power(1.8, -1 * np.absolute(r1 + r2))
        LDFAI.append(ldfai)
    return LDFAI


# SDFAI
def cal_SDFAI(R56, R78):
    SDFAI = []
    for r1, r2 in zip(R56, R78):
        sdfai = (r2 - r1) * (np.absolute(r1) + np.absolute(r2)) * np.power(3.2, -1 * np.absolute(r1 + r2))
        SDFAI.append(sdfai)
    return SDFAI


# 旱涝指数
def cal_Z(R):
    std_r = np.std(R)
    avg_r = np.mean(R)
    n = len(R)
    sum_r = sum(np.power(Ri - avg_r, 3) for Ri in R)
    Cs = sum_r / (n * np.power(std_r, 3))
    Z = []
    # Cs不能为0
    if Cs == 0:
        return None
    for Ri in R:
        z = (6 / Cs) * np.cbrt(((Cs * (Ri - avg_r)) / (2 * std_r)) + 1) - (6 / Cs) + (Cs / 6)
        Z.append(z)
    return Z


if __name__ == '__main__':
    file = 'haixi.xlsx'
    for i in range(1,6):
        dataProc = DataProc(file=file, sheet="Sheet"+str(i))
        dataProc.write()
