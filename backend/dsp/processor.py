import numpy as np
from enum import Enum, auto
import scipy.signal as sgl
from scipy.io import wavfile
import matplotlib.pyplot as plt
import copy


class SignalType(Enum):
    SINE = auto()
    RECTANGULAR_PULSE = auto()
    TRIANGULAR = auto()
    SQUARE = auto()
    NOISE = auto()
    OTHER = auto()


class Signal:
    def __init__(
        self,
        t: np.ndarray,
        signal: np.ndarray,
        duration: tuple[float, float],
        type: SignalType = SignalType.SINE,
        sampling_rate: int = 1000,
        is_digitial: bool = False,
    ) -> None:
        self.t = t
        self.signal = signal
        self.duration = duration
        self.type = type
        self.sampling_rate = sampling_rate
        self.is_digitial = is_digitial

    def sample(self, sampling_rate: int) -> None:
        t = self.t
        self.t = SignalGenerator.get_t(self.duration, sampling_rate)
        self.signal = np.interp(self.t, t, self.signal)

    def quantize(self, levels: int) -> None:
        min_val = np.min(self.signal)
        max_val = np.max(self.signal)
        q = np.linspace(min_val, max_val, levels)
        self.signal = q[np.argmin(np.abs(q[:, None] - self.signal), axis=0)]
        self.is_digitial = True


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
        signal = np.random.normal(scale=amplitude, size=t.shape)
        return Signal(t, signal, duration, SignalType.NOISE, sampling_rate)

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
        return Signal(t, signal, duration, SignalType.SINE, sampling_rate)

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
        return Signal(t, signal, duration, SignalType.RECTANGULAR_PULSE, sampling_rate)

    @staticmethod
    def generate_triangular_wave(
        amplitude: float,
        frequency: float,
        duration: tuple[float, float],
        sampling_rate: int = 1000,
        width: float = 1,
    ) -> Signal:
        t = SignalGenerator.get_t(duration, sampling_rate)
        signal = amplitude * sgl.sawtooth(2 * np.pi * frequency * t, width=width)
        return Signal(t, signal, duration, SignalType.TRIANGULAR, sampling_rate)

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
        return Signal(t, signal, duration, SignalType.SQUARE, sampling_rate)


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
            if signal.is_digitial:
                ax.step(
                    signal.t,
                    signal.signal,
                    where="mid",
                    label=f"{signal.type.name.capitalize()}",
                    color="blue",
                )
            else:
                ax.plot(
                    signal.t,
                    signal.signal,
                    label=f"{signal.type.name.capitalize()}",
                    color="blue",
                )
                ax.scatter(signal.t, signal.signal, color="red", s=10)
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.legend()
            ax.grid(True)
        plt.tight_layout()
        plt.show()

    def plot_spectrums(self) -> None:
        for ax, signal in zip(self.axs, self.signals):
            freq, spectrum = sgl.welch(signal.signal, fs=signal.sampling_rate)
            ax.semilogy(freq, spectrum)
            ax.set_xlabel("Frequency [Hz]")
            ax.set_ylabel("PSD [V**2/Hz]")
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

    sine = SignalGenerator.generate_sine_wave(1, 0.1, (0, 5))
    sine.signal += SignalGenerator.generate_sine_wave(
        4, 0.125, (0, 5), bias=np.pi / 2
    ).signal
    quantized_sine = copy.copy(sine)
    quantized_sine.quantize(8)
    Plotter([sine, quantized_sine]).plot_waveforms()

    sine1 = SignalGenerator.generate_sine_wave(1, 100, (0, 0.5))
    sine2 = SignalGenerator.generate_sine_wave(1, 10, (0, 0.5))
    convolved_signal = np.convolve(sine1.signal, sine2.signal)
    # 卷积
    sine3 = Signal(
        np.linspace(0, 1, len(convolved_signal)),
        convolved_signal,
        (0, 1),
        SignalType.OTHER,
    )
    Plotter([sine1, sine2, sine3]).plot_waveforms()

    sine = SignalGenerator.generate_sine_wave(1, 10, (0, 1), 100)
    signals = [sine]
    for sampling_rate in [5, 10, 20, 40, 80, 100]:
        temp = copy.copy(sine)
        temp.sample(sampling_rate)
        signals.append(copy.copy(temp))
    Plotter(signals).plot_waveforms()

    sampling_rate, signal = wavfile.read("origin.wav")
    signal = signal[:, 0]
    wav = Signal(
        np.linspace(0, len(signal) / sampling_rate, len(signal)),
        signal,
        (0, len(signal) / sampling_rate),
        SignalType.OTHER,
        sampling_rate,
    )
    signals = [wav]
    for sampling_rate in [441, 882, 2205, 11025, 22050]:
        temp = copy.copy(wav)
        temp.sample(sampling_rate)
        signals.append(copy.copy(temp))
    Plotter(signals).plot_waveforms()
    Plotter(signals).plot_spectrums()

    downsampled = copy.copy(wav)
    downsampled.sample(8820)
    resampled = copy.copy(downsampled)
    resampled.sample(44100)
    Plotter([wav, downsampled, resampled]).plot_waveforms()
    Plotter([wav, downsampled, resampled]).plot_spectrums()


if __name__ == "__main__":
    main()
