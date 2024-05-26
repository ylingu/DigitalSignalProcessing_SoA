import os

import sox
from fastapi import UploadFile

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROCESSED_FILES_DIRECTORY = os.path.join(BASE_DIR, "processed_files")


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
    ) -> None:
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
        "blues": (50, 40, 50, 70, 20, 2.5),
        "classical": (50, 75, 85, 70, 40, 3),
        "country": (40, 50, 15, 20, 30, 1.5),
        "disco": (50, 60, 60, 60, 5, 5),
        "hiphop": (20, 70, 40, 30, 50, 2),
        "jazz": (40, 50, 60, 50, 20, 3),
        "metal": (30, 20, 60, 70, 20, 6),
        "pop": (35, 40, 50, 50, 15, 5),
        "reggae": (30, 50, 30, 35, 25, 4),
        "rock": (40, 30, 60, 70, 25, 4),
    }

    def __init__(self, preset: str) -> None:
        super().__init__(*self.presets.get(preset, self.presets["blues"]))
        self.preset = preset


async def apply_reverb(reverb: Reverb, file: UploadFile) -> str:
    input_file = os.path.join(BASE_DIR, file.filename)
    with open(input_file, "wb") as f:
        f.write(await file.read())
    filename_without_extension, extension = os.path.splitext(file.filename)
    # 判断reverb是否存在preset属性
    if hasattr(reverb, "preset"):
        filename = f"{filename_without_extension}_{reverb.preset}{extension}"
    else:
        filename = f"{filename_without_extension}_advanced{extension}"
    output_file = os.path.join(PROCESSED_FILES_DIRECTORY, filename)
    reverb.apply_reverb(input_file, output_file)
    os.remove(input_file)
    return output_file
