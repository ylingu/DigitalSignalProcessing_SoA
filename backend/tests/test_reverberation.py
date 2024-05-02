import os

from dsp import reverberation as rvb


def relpath(path):
    return os.path.join(os.path.dirname(__file__), path)


SOPRANO_FILE = relpath("data/soprano.mp3")
BASS_FILE = relpath("data/bass.wav")
ROCK_FILE = relpath("data/rock.flac")


class TestReverb:
    def test_blues(self):
        reverb = rvb.Reverb()
        assert reverb.reverberance == 50.0
        assert reverb.damping == 50.0
        assert reverb.room_scale == 100.0
        assert reverb.stereo_depth == 100.0
        assert reverb.pre_delay == 0.0
        assert reverb.wet_gain == 0.0
        assert not reverb.wet_only

    def test_apply_reverb(self):
        reverb = rvb.Reverb()
        output_file = relpath("data/BASS_reverb.wav")
        reverb.apply_reverb(BASS_FILE, output_file)
        assert os.path.exists(output_file)
        os.remove(output_file)
        output_file = relpath("data/ROCK_reverb.flac")
        reverb.apply_reverb(ROCK_FILE, output_file)
        assert os.path.exists(output_file)
        os.remove(output_file)
        output_file = relpath("data/SOPRANO_reverb.mp3")
        reverb.apply_reverb(SOPRANO_FILE, output_file)
        assert os.path.exists(output_file)
        os.remove(output_file)

    def test_get_filetype(self):
        assert rvb.Reverb.get_filetype(SOPRANO_FILE) == "mp3"
        assert rvb.Reverb.get_filetype(BASS_FILE) == "wav"
        assert rvb.Reverb.get_filetype(ROCK_FILE) == "flac"

    def test_preset_reverb(self):
        reverb = rvb.PresetReverb("blues")
        assert reverb.reverberance == 50.0
        assert reverb.damping == 50.0
        assert reverb.room_scale == 100.0
        assert reverb.stereo_depth == 100.0
        assert reverb.pre_delay == 0.0
        assert reverb.wet_gain == 0.0
        assert not reverb.wet_only
        assert reverb.preset == "blues"
