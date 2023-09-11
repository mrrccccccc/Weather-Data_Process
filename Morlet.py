import numpy as np
import pywt
import matplotlib.pyplot as plt


def CWT(data, fs=1):
    t = np.arange(0, len(data)) / fs
    n = 2021-len(data)+1
    t = t+n
    wavename = "morl"  # morlet 小波

    totalscale = 256 # 对信号进行小波变换时所用尺度序列的长度
    fc = pywt.central_frequency(wavename)  # 中心频率
    cparam = 2 * fc * totalscale    # 常数c
    scales = cparam / np.arange(totalscale, 1, -1)

    [cwtmatr, frequencies] = pywt.cwt(data, scales, wavename, 1.0 / fs)  # 连续小波变换
    print(abs(cwtmatr))
    plt.figure(figsize=(6, 6))
    fig, ax = plt.subplots()
    plt.xlabel("Time(s)", fontsize = 14)
    plt.ylabel("Amplitude(g)", fontsize=14)
    cs = ax.contourf(t, 1/frequencies, abs(cwtmatr), cmap="rainbow", vmin=0, vmax=4)
    plt.xlabel("Time(year)")
    plt.ylabel("cycle(a)")
    plt.tight_layout()
    plt.axis([n, 2021, 2, 50])
    plt.savefig("." + "_CWT" + ".png")
    fig.colorbar(cs)
    plt.show()

