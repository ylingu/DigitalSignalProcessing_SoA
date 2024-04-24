import sox


class Reverb:
    def __init__(  # noqa: PLR0913
        self,
        reverberance: float = 50.0,
        damping: float = 50.0,
        room_scale: float = 100.0,
        stereo_depth: float = 100.0,
        pre_delay: float = 0.0,
        wet_gain: float = 0.0,
        wet_only: bool = False,
    ):
        self.reverberance = reverberance
        self.damping = damping
        self.wet_gain = wet_gain
        self.room_scale = room_scale
        self.stereo_depth = stereo_depth
        self.pre_delay = pre_delay
        self.wet_only = wet_only

    def apply_reverb(self, input_file: str, output_file: str) -> None:
        tfm = sox.Transformer()
        tfm.set_input_format(file_type=self.get_filetype(input_file))
        tfm.set_output_format(file_type=self.get_filetype(output_file))
        tfm.reverb(
            self.reverberance,
            self.damping,
            self.room_scale,
            self.stereo_depth,
            self.pre_delay,
            self.wet_gain,
            self.wet_only,
        )
        tfm.build(input_file, output_file)

    @staticmethod
    def get_filetype(file: str) -> str:
        return file.split(".")[-1]


class PresetReverb(Reverb):
    presets: dict[str, tuple[float, float, float, float, float, float]] = {
        "default": (50, 50, 100, 100, 0, 0),
    }

    def __init__(self, preset: str):
        super().__init__(*self.presets.get(preset, self.presets["default"]))
        self.preset = preset
