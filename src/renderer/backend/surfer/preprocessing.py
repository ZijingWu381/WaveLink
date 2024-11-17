import pandas as pd
import numpy as np
from scipy.signal import butter, filtfilt
import os

from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-I', '--input_file', type=str, help='input raw data file name')
parser.add_argument('-O', '--output_file', type=str, help='output preprocessed data file name')

# Configurable Variables 
ORIGINAL_FS = 125  # Original sampling rate
TARGET_FS = 50     # Target sampling rate
LOWCUT = 0.1       # Low cutoff frequency for bandpass filter (Hz)
HIGHCUT = 20       # High cutoff frequency for bandpass filter (Hz)
FILTER_ORDER = 2   # Order of the bandpass filter
EXCLUDE_CHANNELS = [0, 11]  # Channels to exclude from filtering

# Define bandpass filter function
def bandpass_filter(data, lowcut, highcut, fs, order):
    """
    Bandpass filter to remove noise outside the frequency range of interest.
    """
    nyquist = 0.5 * fs
    b, a = butter(order, [lowcut / nyquist, highcut / nyquist], btype='band')
    return filtfilt(b, a, data)


def preprocess_eeg(input_file_path, output_file_path, original_fs, target_fs, lowcut, highcut, filter_order, exclude_channels):
    """
    Preprocess EEG data: down-sample, remove DC offset, apply bandpass filter, and handle excluded channels.
    """
    print(f"Loading EEG data from {input_file_path}...")
    eeg_data = pd.read_csv(input_file_path)

    # Separate excluded channels
    excluded_data = eeg_data.iloc[:, exclude_channels]
    data_to_process = eeg_data.drop(columns=eeg_data.columns[exclude_channels])

    # Step 1: Down-sample to TARGET_FS
    print(f"Down-sampling data to {target_fs} Hz...")
    downsample_factor = int(original_fs / target_fs)
    excluded_data_downsampled = excluded_data.iloc[::downsample_factor, :].reset_index(drop=True)
    data_downsampled = data_to_process.iloc[::downsample_factor, :].reset_index(drop=True)

    # Step 2: Remove DC offset (mean removal)
    print("Removing DC offset...")
    data_detrended = data_downsampled - data_downsampled.mean()

    # Step 3: Apply bandpass filter to each channel
    print(f"Applying bandpass filter: {lowcut}–{highcut} Hz...")
    filtered_data = data_detrended.copy()
    for col in filtered_data.columns:
        filtered_data[col] = bandpass_filter(filtered_data[col], lowcut=lowcut, highcut=highcut, fs=target_fs, order=filter_order)

    # Combine excluded channels with processed channels
    print("Combining excluded and processed data...")
    combined_data = pd.concat([excluded_data_downsampled, filtered_data], axis=1)

    # Step 4: Save the preprocessed data to a CSV file
    print(f"Saving preprocessed data to {output_file_path}...")
    combined_data.to_csv(output_file_path, index=False)
    print(f"Preprocessed data saved to: {output_file_path}")


# Main function to process multiple files
def main():
    args = parser.parse_args()
    current_file_directory = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(current_file_directory, '../data/')
    input_file_path = os.path.join(data_dir, 'raw', args.input_file)
    output_file_path = os.path.join(data_dir, 'processed', args.output_file)

    if not os.path.exists(input_file_path):
        raise FileNotFoundError(f"Input file {input_file_path} does not exist. Skipping...")
    else:
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


if __name__ == "__main__":
    main()