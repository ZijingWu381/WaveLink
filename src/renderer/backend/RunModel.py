from surfer.preprocessing import preprocess_eeg
import os
from surfer.main import run
# Configurable Variables 
ORIGINAL_FS = 125  # Original sampling rate
TARGET_FS = 50     # Target sampling rate
LOWCUT = 0.1       # Low cutoff frequency for bandpass filter (Hz)
HIGHCUT = 20       # High cutoff frequency for bandpass filter (Hz)
FILTER_ORDER = 2   # Order of the bandpass filter
EXCLUDE_CHANNELS = [0, 11]  # Channels to exclude from filtering
current_file_directory = os.path.dirname(os.path.abspath(__file__))


def main_func():
    for file in ['data_output_1.csv', 'data_output_2.csv']:

        input_file_path = os.path.join(current_file_directory,"tempdata", file)

        output_file_path = os.path.join(current_file_directory, "moretemp", f"preprocessed_{file}")
        if os.path.exists(output_file_path):
            os.remove(output_file_path)
        # Preprocess EEG data
        preprocess_eeg(
                    input_file_path=input_file_path,
                    output_file_path=output_file_path,
                    original_fs=ORIGINAL_FS,
                    target_fs=TARGET_FS,
                    lowcut=LOWCUT,
                    highcut=HIGHCUT,
                    filter_order=FILTER_ORDER,
                    exclude_channels=EXCLUDE_CHANNELS
                )
        os.remove(input_file_path)
    return run()