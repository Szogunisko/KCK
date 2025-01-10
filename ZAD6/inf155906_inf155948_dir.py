import sys
import os
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


def answer(base_freq, filename):

    good_answer = filename.split('_')[-1][0]

    if(base_freq < pitch_cutoff):
        our_answer = 'M'
    else:
        our_answer = 'K'

    if our_answer != good_answer:
        return False, our_answer, good_answer

    return True, our_answer


def process_directory(folder_path):
    results = {
        'correct': 0,
        'wrong': 0,
        'true_female': 0,  # Kobiety prawidłowo rozpoznane
        'missed_female': 0,  # Kobiety uznane za mężczyzn
        'true_male': 0,  # Mężczyźni prawidłowo rozpoznani
        'false_male': 0,  # Mężczyźni uznani za kobiety
    }

    for file_name in os.listdir(folder_path):
        if file_name.endswith(".wav"):
            try:
                file_path = os.path.join(folder_path, file_name)

                base_frequency = process_audio_with_hps(file_path)
                if base_frequency is None:
                    continue

                is_correct, final_answer = answer(base_frequency, file_name)

                print(final_answer)

                if is_correct:
                    results['correct'] += 1
                    if final_answer == 'K':
                        results['true_female'] += 1
                    else:
                        results['true_male'] += 1
                else:
                    results['wrong'] += 1
                    if final_answer == 'M':
                        results['missed_female'] += 1
                    else:
                        results['false_male'] += 1

            except Exception as e:
                print(f"Problem z plikiem: {file_name}: {e}")

    print(f"Poprawne klasyfikacje: {results['correct']}")
    print(f"Błędne klasyfikacje: {results['wrong']}")
    print(f"Kobieta rozpoznana prawidłowo: {results['true_female']}")
    print(f"Kobieta rozpoznana jako mężczyzna: {results['missed_female']}")
    print(f"Mężczyzna rozpoznany prawidłowo: {results['true_male']}")
    print(f"Mężczyzna rozpoznany jako kobieta: {results['false_male']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Podaj ścieżkę do katalogu z plikami .wav.")
        sys.exit(1)

    input_dir = sys.argv[1]
    process_directory(input_dir)
