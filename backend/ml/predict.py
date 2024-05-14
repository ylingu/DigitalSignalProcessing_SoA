import librosa
import numpy as np
import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from xgboost import XGBClassifier


def preprocess(scaler: MinMaxScaler, y: np.ndarray) -> pd.DataFrame:
    features = {}
    features["length"] = 0
    # Chroma STFT
    chroma_stft = librosa.feature.chroma_stft(y=y)
    features["chroma_stft_mean"] = np.mean(chroma_stft)
    features["chroma_stft_var"] = np.var(chroma_stft)
    # RMS energy
    rms = librosa.feature.rms(y=y)
    features["rms_mean"] = np.mean(rms)
    features["rms_var"] = np.var(rms)
    # Spectral centroid
    spectral_centroid = librosa.feature.spectral_centroid(y=y)
    features["spectral_centroid_mean"] = np.mean(spectral_centroid)
    features["spectral_centroid_var"] = np.var(spectral_centroid)
    # Spectral bandwidth
    spectral_bandwidth = librosa.feature.spectral_bandwidth(y=y)
    features["spectral_bandwidth_mean"] = np.mean(spectral_bandwidth)
    features["spectral_bandwidth_var"] = np.var(spectral_bandwidth)
    # Spectral rolloff
    rolloff = librosa.feature.spectral_rolloff(y=y)
    features["rolloff_mean"] = np.mean(rolloff)
    features["rolloff_var"] = np.var(rolloff)
    # Zero-crossing rate
    zero_crossing_rate = librosa.feature.zero_crossing_rate(y)
    features["zero_crossing_rate_mean"] = np.mean(zero_crossing_rate)
    features["zero_crossing_rate_var"] = np.var(zero_crossing_rate)
    # Harmonic and percussive components
    y_harm, y_perc = librosa.effects.hpss(y)
    features["harmony_mean"] = np.mean(y_harm)
    features["harmony_var"] = np.var(y_harm)
    features["perceptr_mean"] = np.mean(y_perc)
    features["perceptr_var"] = np.var(y_perc)
    # Tempo
    tempo, _ = librosa.beat.beat_track(y=y)
    features["tempo"] = tempo
    # MFCCs
    mfccs = librosa.feature.mfcc(y=y)
    for i, mfcc in enumerate(mfccs, start=1):
        features[f"mfcc{i}_mean"] = np.mean(mfcc)
        features[f"mfcc{i}_var"] = np.var(mfcc)
    df = pd.DataFrame([features])
    df = pd.DataFrame(scaler.transform(df), columns=df.columns)
    return df


GENRE_MAP = {
    0: "blues",
    1: "classical",
    2: "country",
    3: "disco",
    4: "hiphop",
    5: "jazz",
    6: "metal",
    7: "pop",
    8: "reggae",
    9: "rock",
}


def predict(scaler: MinMaxScaler, model: XGBClassifier, y: np.ndarray) -> str:
    data = preprocess(scaler, y)
    res = model.predict(data)
    genre = GENRE_MAP[res[0]]
    return genre
