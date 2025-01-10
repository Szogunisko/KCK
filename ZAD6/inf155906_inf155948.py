import sys
import numpy as np
from scipy.io import wavfile
from scipy.fft import fft, ifft
from scipy.signal import decimate
import warnings

# Wyłączanie wszelkich ostrzeżeń
warnings.filterwarnings("ignore")

pitch_cutoff = 179  # Próg częstotliwości dla klasyfikacji płci


def process_audio_with_hps(file_path):
    sampling_rate, audio_signal = wavfile.read(file_path)

    if audio_signal.ndim > 1:  # Jeśli sygnał ma więcej niż jeden kanał, weź pierwszy
        audio_signal = audio_signal[:, 0]

    spectrum = np.abs(fft(audio_signal))
    n = len(spectrum)
    spectrum = spectrum[:n // 2]
    spectrum /= n / 2
    spectrum[0] /= 2
    freqs = np.arange(len(spectrum)) / n * sampling_rate

    cutoff = -1
    for i in range(len(freqs)):
        if freqs[i] > 2000:
            cutoff = i
            break

    if spectrum is not None and freqs is not None:
        low_cut_idx = -1
        for i in range(len(freqs)):
            if freqs[i] > 80:
                low_cut_idx = i
                break
        spectrum[:low_cut_idx] = 0

        spectrum = spectrum[:cutoff]

        hps_spectrum = spectrum.copy()
        for factor in range(2, 5):
            reduced = decimate(spectrum, factor)
            hps_spectrum[:len(reduced)] *= reduced

        max_idx = 0
        max_value = hps_spectrum[0]
        limit = -1
        for i in range(len(freqs)):
            if freqs[i] > 350:
                limit = i
                break
        for i in range(1, limit):
            if hps_spectrum[i] > max_value:
                max_value = hps_spectrum[i]
                max_idx = i

        base_frequency = freqs[max_idx]
        return base_frequency
    return None

def run(file_path):
    base_frequency = process_audio_with_hps(file_path)
    if base_frequency is None:
        return "M"
    else:
        if(base_frequency < pitch_cutoff):
            return 'M'
        else:
            return 'K'
        
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Podaj ścieżkę do pliku")
        sys.exit(1)
    file_path = sys.argv[1]
    print(run(file_path))