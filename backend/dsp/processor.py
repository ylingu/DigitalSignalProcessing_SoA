from __future__ import annotations

import copy

import matplotlib.pyplot as plt
import numpy as np
import scipy.signal as sgl
from scipy.interpolate import interp1d
from scipy.io import wavfile


class Signal:
    def __init__(
        self,
        t: np.ndarray,
        signal: np.ndarray,
        duration: tuple[float, float],
        sampling_rate: int = 1000,
    ) -> None:
        self.t = t
        self.signal = signal
        self.duration = duration
        self.sampling_rate = sampling_rate

    def __add__(self, other: Signal) -> Signal:
        if self.duration != other.duration:
            raise ValueError("Signals must have the same duration")
        if self.sampling_rate != other.sampling_rate:
            raise ValueError("Signals must have the same sampling rate")
        signal = self.signal + other.signal
        return Signal(self.t, signal, self.duration, self.sampling_rate)

    def sample(self, sampling_rate: int) -> None:
        t = self.t
        self.t = SignalGenerator.get_t(self.duration, sampling_rate)
        self.signal = np.interp(self.t, t, self.signal)
        self.sampling_rate = sampling_rate

    def quantize(self, levels: int) -> None:
        min_val = np.min(self.signal)
        max_val = np.max(self.signal)
        q = np.linspace(min_val, max_val, levels)
        self.signal = q[np.argmin(np.abs(q[:, None] - self.signal), axis=0)]

    def fft(self, use_interpolation: bool = False) -> None:
        signal, sampling_rate = self.signal, self.sampling_rate
        if use_interpolation:
            f = interp1d(self.t, self.signal, kind="cubic", fill_value="extrapolate")
            sampling_rate = 4 * self.sampling_rate
            t = SignalGenerator.get_t(self.duration, sampling_rate)
            signal = f(t)
        self.freqs = np.fft.fftfreq(len(signal), 1 / sampling_rate)
        self.spectrum = np.abs(np.fft.fft(signal))


class SignalGenerator:
    @staticmethod
    def get_t(duration: tuple[float, float], sampling_rate: int = 1000) -> np.ndarray:
        return np.linspace(
            duration[0],
            duration[1],
            int(sampling_rate * (duration[1] - duration[0])),
            endpoint=False,
        )

    @staticmethod
    def generate_noise(
        amplitude: float, duration: tuple[float, float], sampling_rate: int = 1000
    ) -> Signal:
        t = SignalGenerator.get_t(duration, sampling_rate)
        signal = np.random.default_rng().normal(scale=amplitude, size=t.shape)
        return Signal(t, signal, duration, sampling_rate)

    @staticmethod
    def generate_sine_wave(
        amplitude: float,
        frequency: float,
        duration: tuple[float, float],
        sampling_rate: int = 1000,
        bias: float = 0,
    ) -> Signal:
        t = SignalGenerator.get_t(duration, sampling_rate)
        signal = amplitude * np.sin(2 * np.pi * frequency * t + bias)
        return Signal(t, signal, duration, sampling_rate)

    @staticmethod
    def generate_rectangular_pulse(
        amplitude: float,
        duration: tuple[float, float],
        pulse_width: float,
        sampling_rate: int = 1000,
    ) -> Signal:
        t = SignalGenerator.get_t(duration, sampling_rate)
        signal = (
            amplitude
            * (np.sign(t + pulse_width / 2) - np.sign(t - pulse_width / 2))
            / 2
        )
        return Signal(t, signal, duration, sampling_rate)

    @staticmethod
    def generate_triangular_wave(
        amplitude: float,
        frequency: float,
        duration: tuple[float, float],
        sampling_rate: int = 1000,
        width: int = 1,
    ) -> Signal:
        t = SignalGenerator.get_t(duration, sampling_rate)
        signal = amplitude * sgl.sawtooth(2 * np.pi * frequency * t, width=width)
        return Signal(t, signal, duration, sampling_rate)

    @staticmethod
    def generate_square_wave(
        amplitude: float,
        frequency: float,
        duration: tuple[float, float],
        sampling_rate: int = 1000,
        duty: float = 0.5,
    ) -> Signal:
        t = SignalGenerator.get_t(duration, sampling_rate)
        signal = amplitude * sgl.square(2 * np.pi * frequency * t, duty=duty)
        return Signal(t, signal, duration, sampling_rate)


class Plotter:
    def __init__(
        self,
        signals: list[Signal],
    ) -> None:
        self.signals = signals
        self.fig, self.axs = plt.subplots(
            len(signals), 1, figsize=(10, 2.5 * len(signals))
        )
        if len(signals) == 1:
            self.axs = [self.axs]

    def plot_waveforms(self) -> None:
        for ax, signal in zip(self.axs, self.signals):
            t = signal.t
            if len(signal.t) != len(signal.signal):
                t = np.linspace(
                    signal.duration[0],
                    signal.duration[1],
                    len(signal.signal),
                    endpoint=False,
                )
            ax.plot(
                t,
                signal.signal,
                color="blue",
            )
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_spectrums(self) -> None:
        for ax, signal in zip(self.axs, self.signals):
            if not hasattr(signal, "freqs") or not hasattr(signal, "spectrum"):
                signal.fft()
            ax.semilogy(signal.freqs, signal.spectrum)
            ax.set_xlabel("Frequency [Hz]")
            ax.set_ylabel("FFT [V/Hz]")
        plt.tight_layout()
        plt.show()


def main():
    sine = SignalGenerator.generate_sine_wave(5, 3, (0, 10))
    sine_noise = copy.deepcopy(sine)
    sine_noise.signal += SignalGenerator.generate_noise(1, (0, 10)).signal
    rect_pulse = SignalGenerator.generate_rectangular_pulse(13, (-6, 6), 2)
    triangular = SignalGenerator.generate_triangular_wave(1, 0.125, (0, 12), 1000, 0.7)
    square = SignalGenerator.generate_square_wave(1, 1 / 6, (0, 12), 1000, 0.3)
    Plotter([sine, sine_noise, rect_pulse, triangular, square]).plot_waveforms()

    sine = SignalGenerator.generate_sine_wave(1, 0.1, (0, 10))
    sine += SignalGenerator.generate_sine_wave(4, 0.125, (0, 10), bias=np.pi / 2)
    quantized_sine = copy.copy(sine)
    quantized_sine.quantize(8)
    Plotter([sine, quantized_sine]).plot_waveforms()

    sine1 = SignalGenerator.generate_sine_wave(1, 100, (0, 0.5))
    sine2 = SignalGenerator.generate_sine_wave(1, 10, (0, 0.5))
    convolved_signal = np.convolve(sine1.signal, sine2.signal)
    sine3 = Signal(
        np.linspace(0, 1, len(convolved_signal)),
        convolved_signal,
        (0, 1),
    )
    Plotter([sine1, sine2, sine3]).plot_waveforms()

    sine = SignalGenerator.generate_sine_wave(1, 10, (0, 1), 1000, np.pi / 6)
    signals = [sine]
    for sampling_rate in [10, 20, 21, 40, 80, 200]:
        temp = copy.copy(sine)
        temp.sample(sampling_rate)
        temp.fft(True)
        signals.append(copy.copy(temp))
    Plotter(signals).plot_waveforms()
    Plotter(signals).plot_spectrums()
    for signal in signals:
        signal.spectrum[np.abs(signal.freqs) > 11] = 0  # noqa: PLR2004
        signal.signal = np.fft.ifft(signal.spectrum).real
    Plotter(signals).plot_waveforms()

    sampling_rate, signal = wavfile.read("tests/data/origin.wav")
    signal = signal[:, 0]
    wav = Signal(
        np.linspace(0, len(signal) / sampling_rate, len(signal)),
        signal,
        (0, len(signal) / sampling_rate),
        sampling_rate,
    )
    signals = [wav]
    for sampling_rate in [441, 882, 2205, 11025, 22050]:
        temp = copy.copy(wav)
        temp.sample(sampling_rate)
        signals.append(copy.copy(temp))
    Plotter(signals).plot_waveforms()
    Plotter(signals).plot_spectrums()


if __name__ == "__main__":
    main()
