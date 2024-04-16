import numpy as np
from enum import Enum, auto
from scipy import signal
import matplotlib.pyplot as plt


class SignalGenerator:
    def __init__(
        self,
        amplitude: float,
        frequency: float,
        duration: tuple[float, float],
        sampling_rate: float = 1000,
        noise_amplitude: float = 0,
    ) -> None:
        self.amplitude = amplitude
        self.frequency = frequency
        self.duration = duration
        self.sampling_rate = sampling_rate
        self.noise_amplitude = noise_amplitude
        self.t = np.linspace(
            duration[0],
            duration[1],
            int(sampling_rate * (duration[1] - duration[0])),
            endpoint=False,
        )

    def generate_noise(self) -> np.ndarray:
        return np.random.normal(scale=self.noise_amplitude, size=self.t.shape)

    def generate_sine_wave(self, b: float = 0) -> np.ndarray:
        return (
            self.amplitude * np.sin(2 * np.pi * self.frequency * self.t + b)
            + self.generate_noise()
        )

    def generate_rectangular_pulse(self, pulse_width: float) -> np.ndarray:
        return (
            self.amplitude
            * (np.sign(self.t + pulse_width / 2) - np.sign(self.t - pulse_width / 2))
            / 2
            + self.generate_noise()
        )

    def generate_triangular_wave(self, width: int = 1) -> np.ndarray:
        return (
            self.amplitude
            * signal.sawtooth(2 * np.pi * self.frequency * self.t, width=width)
            + self.generate_noise()
        )

    def generate_square_wave(self, duty: float = 0.5) -> np.ndarray:
        return (
            self.amplitude
            * signal.square(2 * np.pi * self.frequency * self.t, duty=duty)
            + self.generate_noise()
        )

    @staticmethod
    def sample(
        signal: np.ndarray, sampling_rate: int, duration: tuple[float, float]
    ) -> np.ndarray:
        t = np.linspace(
            duration[0],
            duration[1],
            int(sampling_rate * (duration[1] - duration[0])),
            endpoint=False,
        )
        return np.interp(
            t, np.linspace(0, duration[1] - duration[0], len(signal)), signal
        )

    @staticmethod
    def quantize(signal: np.ndarray, levels: int) -> np.ndarray:
        min_val = np.min(signal)
        max_val = np.max(signal)
        q = np.linspace(min_val, max_val, levels)
        quantized_signal = q[np.argmin(np.abs(q[:, None] - signal), axis=0)]
        return quantized_signal


class SignalType(Enum):
    SINE = auto()
    RECTANGULAR_PULSE = auto()
    TRIANGULAR = auto()
    SQUARE = auto()
    QUANTIZED = auto()


class WaveformPlotter:
    def __init__(
        self,
        t_list: list[np.ndarray],
        signals: list[np.ndarray],
        signal_types: list[SignalType],
    ) -> None:
        assert len(t_list) == len(signals) == len(signal_types)
        self.t_list = t_list
        self.signals = signals
        self.signal_types = signal_types
        self.fig, self.axs = plt.subplots(len(t_list), 1, figsize=(12, 3 * len(t_list)))
        if len(t_list) == 1:
            self.axs = [self.axs]

    def plot_waveforms(self) -> None:
        for ax, t, sig, type in zip(
            self.axs, self.t_list, self.signals, self.signal_types
        ):
            if type == SignalType.QUANTIZED:
                ax.step(
                    t, sig, where="mid", label=f"{type.name.capitalize()}", color="blue"
                )
            else:
                ax.plot(t, sig, label=f"{type.name.capitalize()}", color="blue")
                ax.scatter(t, sig, color="red", s=10)
            ax.set_title(f"{type.name.capitalize()} Signal")
            ax.set_xlabel("Time (s)")
            ax.set_ylabel("Amplitude")
            ax.legend()
            ax.grid(True)
        plt.tight_layout()
        plt.show()


def main():
    sine_noise = SignalGenerator(
        amplitude=1, frequency=5, duration=(0, 1), noise_amplitude=0.1
    )
    sine = SignalGenerator(amplitude=5, frequency=3, duration=(0, 1))
    rect_pulse = SignalGenerator(amplitude=13, frequency=2, duration=(-6, 6))
    triangular = SignalGenerator(amplitude=1, frequency=0.125, duration=(0, 12))
    square = SignalGenerator(amplitude=1, frequency=1 / 6, duration=(0, 12))

    WaveformPlotter(
        [sine_noise.t, sine.t, rect_pulse.t, triangular.t, square.t],
        [
            sine_noise.generate_sine_wave(),
            sine.generate_sine_wave(),
            rect_pulse.generate_rectangular_pulse(2),
            triangular.generate_triangular_wave(0.7),
            square.generate_square_wave(0.3),
        ],
        [
            SignalType.SINE,
            SignalType.SINE,
            SignalType.RECTANGULAR_PULSE,
            SignalType.TRIANGULAR,
            SignalType.SQUARE,
        ],
    ).plot_waveforms()

    sine_signal = SignalGenerator(
        amplitude=1, frequency=0.1, duration=(0, 5)
    ).generate_sine_wave() + SignalGenerator(
        amplitude=4, frequency=0.125, duration=(0, 5)
    ).generate_sine_wave(np.pi / 2)
    quantized_signal = SignalGenerator.quantize(sine_signal, 8)
    WaveformPlotter(
        [
            SignalGenerator(amplitude=1, frequency=0.1, duration=(0, 5)).t,
            SignalGenerator(amplitude=1, frequency=0.1, duration=(0, 5)).t,
        ],
        [sine_signal, quantized_signal],
        [SignalType.SINE, SignalType.QUANTIZED],
    ).plot_waveforms()

    sine1 = SignalGenerator(amplitude=1, frequency=100, duration=(0, 0.5))
    sine2 = SignalGenerator(amplitude=1, frequency=10, duration=(0, 0.5))
    # 卷积
    sine3 = np.convolve(sine1.generate_sine_wave(), sine2.generate_sine_wave())
    WaveformPlotter(
        [sine1.t, sine2.t, np.linspace(-0.5, 1, len(sine3))],
        [sine1.generate_sine_wave(), sine2.generate_sine_wave(), sine3],
        [SignalType.SINE, SignalType.SINE, SignalType.SINE],
    ).plot_waveforms()

    sine = SignalGenerator(
        amplitude=1, frequency=10, duration=(0, 1), sampling_rate=100
    )
    sine_signal = sine.generate_sine_wave(0.3)
    t_list, signals = [sine.t], [sine_signal]
    for sampling_rate in [5, 10, 20, 40, 80, 100]:
        t_list.append(
            SignalGenerator(
                amplitude=1, frequency=10, duration=(0, 1), sampling_rate=sampling_rate
            ).t
        )
        signals.append(SignalGenerator.sample(sine_signal, sampling_rate, (0, 1)))
        print(f"Signal sampled at {sampling_rate} Hz")
    WaveformPlotter(t_list, signals, [SignalType.SINE] * len(signals)).plot_waveforms()


if __name__ == "__main__":
    main()
