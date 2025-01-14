import sys
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft
from scipy.signal import decimate
import warnings

# Wyłączanie wszelkich ostrzeżeń
warnings.filterwarnings("ignore")
pitch_cutoff = 179  # Próg częstotliwości dla klasyfikacji płci

def process_audio_with_hps(file_path):
    w, audio_signal = wavfile.read(file_path)

    if audio_signal.ndim >= 2:  # Jeśli sygnał ma 2 kanały lub więcej, weź pierwszy
        audio_signal = audio_signal[:, 0]

    signal1 = fft(audio_signal)
    n = len(signal1)
    signal1 = signal1[:n // 2]
    signal1 = 2*np.abs(signal1)/n
    freqs = np.arange(n)/n* w

    if signal1 is None or freqs is None:
        return None
    cutoff = -1
    for i in range(len(freqs)):
        if freqs[i] > 80:
            cutoff = i
            break
    signal1[:cutoff] = 0

    hps_spectrum = signal1.copy()
    for factor in range(2, 5):
        reduced = decimate(signal1, factor)
        hps_spectrum[:len(reduced)] *= reduced

    max_value = hps_spectrum[0]
    for i in range(1, n//2):
        if hps_spectrum[i] > max_value:
            max_value = hps_spectrum[i]
            max_index = i

    return freqs[max_index]

def run(file_path):
    try:
        base_frequency = process_audio_with_hps(file_path)
        if base_frequency is None:
            return "K"
        else:
            if base_frequency < pitch_cutoff:
                return 'M'
            else:
                return 'K'
    except:
        return "K"
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Podaj ścieżkę do pliku")
        sys.exit(1)
    file_path = sys.argv[1]
    print(run(file_path))