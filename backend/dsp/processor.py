import numpy as np
import matplotlib.pyplot as plt

# 模拟信号参数
frequency = 5  # 频率（Hz）
sampling_rate = 100  # 采样率（Hz）
duration = 1  # 信号持续时间（秒）
t = np.linspace(0, duration, int(sampling_rate * duration), endpoint=False)

# 原始模拟信号（正弦波）
analog_signal = np.sin(2 * np.pi * frequency * t)

# 添加噪声的参数
noise_amplitude = 0.05  # 噪声幅度

# 生成噪声
noise = np.random.normal(scale=noise_amplitude, size=t.shape)

# 将噪声添加到原始模拟信号中
noisy_signal = analog_signal + noise

# 打印原始模拟信号的前10个样本
print("Original Analog Signal (First 10 Samples):")
print(analog_signal[:10])

# 绘制原始模拟信号和采样点
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(t,noisy_signal, label="Original Analog Signal", color="blue")
plt.scatter(t, noisy_signal, color="red", s=10)  # 采样点用红色散点表示
plt.title("Original Analog Signal with Sampling Points")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

# A/D转换参数
quantization_levels = 8  # 量化级别
quantization_step = 1 / (quantization_levels - 1)  # 量化步长

# 量化步骤
quantized_signal = np.round(noisy_signal / quantization_step) * quantization_step

# 输出量化信号的前10个样本
print("Quantized Signal (First 10 Samples):")
print(quantized_signal[:10])

# 绘制量化信号
plt.subplot(2, 1, 2)
plt.step(t, quantized_signal, where="mid", label="Quantized Signal")
plt.title("Quantized Signal")
plt.xlabel("Time (s)")
plt.ylabel("Amplitude")
plt.legend()
plt.grid(True)

# 显示图形
plt.tight_layout()
plt.show()