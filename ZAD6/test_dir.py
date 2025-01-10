import os
import inf155906_inf155948  # Import programu jako modułu

correctAnswers = 0
files = 0

def process_folder(folder_path):
    global correctAnswers, files
    if not os.path.isdir(folder_path):
        print(f"Błąd: Ścieżka '{folder_path}' nie jest folderem.")
        return

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            good_answer = file_path.split('_')[-1][0]
            our_answer = inf155906_inf155948.run(file_path)  # Wywołanie funkcji bezpośrednio
            print(our_answer)
            if our_answer == good_answer:
                correctAnswers += 1
            files += 1

if __name__ == "__main__":
    import sys
    folder = sys.argv[1]
    process_folder(folder)
    print(f"Poprawne klasyfikacje: {correctAnswers}")
    print(f"Skuteczność: {correctAnswers / files * 100}%")
