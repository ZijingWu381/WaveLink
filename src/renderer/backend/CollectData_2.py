import threading
import time
import numpy as np
import pandas as pd
import os  # For checking and deleting files
from brainflow.board_shim import BoardShim, BrainFlowInputParams, BoardIds
import logging


def save_data_to_csv(data, filename="raw_eeg_data.csv"):
    """
    Save the raw EEG data to a CSV file using pandas.
    """
    # Append the DataFrame to the CSV file
    with open(filename, mode='w', newline='') as f:
        data.to_csv(f, index=False, header=f.tell() == 0)  # Write header only if the file is empty
    print(f"Raw data appended to {filename}")


class EEGProcessor:
    def __init__(self, serial_port, output_file, streaming_duration, interval=10):
        self.serial_port = serial_port
        self.output_file = output_file
        self.streaming_duration = streaming_duration
        self.interval = interval  # Interval in seconds
        self.start_time = time.time()
        self.timer = None
        self.board = None
    
    def check_and_delete_file(self):
        """
        Check if the output file exists and delete it if it does.
        """
        if os.path.exists(self.output_file):
            print(f"File {self.output_file} already exists. Deleting it...")
            os.remove(self.output_file)
            print(f"File {self.output_file} has been deleted.")
        else:
            print(f"File {self.output_file} does not exist. Proceeding to initialize...")

    def initialize_board(self):
        """
        Initialize the BrainFlow board and start streaming data.
        """
        self.check_and_delete_file()
        BoardShim.enable_board_logger()
        params = BrainFlowInputParams()
        params.serial_port = self.serial_port
        self.board = BoardShim(BoardIds.NEUROPAWN_KNIGHT_BOARD, params)

        print("Preparing session...")
        self.board.prepare_session()
        print("Starting data stream...")
        self.board.start_stream(450000)

        print("Board prepared:", self.board.is_prepared())

        # Configure specific channels
        self.configure_channels()

    def configure_channels(self):
        """
        Configure specific channels with desired gain settings.
        """
        print("Configuring channels...")
        time.sleep(3)
        self.board.config_board("chon_1_12")
        time.sleep(1)
        self.board.config_board("rldadd_1")  # Example: Configure channel 1 with gain 12
        time.sleep(1)
        self.board.config_board("chon_2_12")  # Example: Configure channel 1 with gain 12
        time.sleep(1)
        self.board.config_board("rldadd_2")  # Example: Configure channel 1 with gain 12
        time.sleep(1)
        self.board.config_board("chon_3_12")  # Example: Configure channel 3 with gain 12
        time.sleep(1)
        self.board.config_board("rldadd_3")  # Example: Configure channel 1 with gain 12
        time.sleep(1)
        self.board.config_board("chon_4_12")  # Example: Configure channel 3 with gain 12
        time.sleep(1)
        self.board.config_board("rldadd_4")  # Example: Configure channel 1 with gain 12
        time.sleep(1)
        self.board.config_board("chon_5_12")  # Example: Configure channel 5 with gain 12
        time.sleep(1)
        self.board.config_board("rldadd_5")  # Example: Configure channel 1 with gain 12
        time.sleep(1)
        self.board.config_board("chon_6_12")  # Example: Configure channel 3 with gain 12
        time.sleep(1)
        self.board.config_board("rldadd_6")  # Example: Configure channel 1 with gain 12
        time.sleep(1)
        self.board.config_board("chon_7_12")  # Example: Configure channel 7 with gain 12
        time.sleep(1)
        self.board.config_board("rldadd_7")  # Example: Configure channel 1 with gain 12
        time.sleep(1)
        self.board.config_board("chon_8_12")  # Example: Configure channel 3 with gain 12
        time.sleep(1)
        self.board.config_board("rldadd_8")  # Example: Configure channel 1 with gain 12
        time.sleep(1)
        print("Channels configured.")

    def process_and_save_data(self):
        """
        Read raw data from the board and save it to a CSV file.
        """
        elapsed_time = time.time() - self.start_time
        if elapsed_time >= self.streaming_duration:
            print("Completed streaming duration.")
            self.stop_processing()
            return

        # Read raw data from the board
        print(f"Processing data at {elapsed_time:.2f} seconds...")
        raw_data = np.array(self.board.get_current_board_data(1250))
        df_raw = pd.DataFrame(raw_data).transpose()

        # Save the raw data to CSV
        save_data_to_csv(df_raw, self.output_file)

        # Schedule the next execution
        self.timer = threading.Timer(self.interval, self.process_and_save_data)
        self.timer.start()

    def start_processing(self):
        """
        Start the periodic data processing.
        """
        self.process_and_save_data()  # Start immediately

    def stop_processing(self):
        """
        Stop the periodic data processing, save remaining data, and release the board session.
        """
        if self.timer:
            self.timer.cancel()

        # Save any remaining data
        print("Saving final data before stopping...")
        raw_data = np.array(self.board.get_current_board_data(1250))
        df_raw = pd.DataFrame(raw_data).transpose()
        save_data_to_csv(df_raw, self.output_file)

        # Release the board
        print("Releasing session...")
        if self.board and self.board.is_prepared():
            self.board.release_session()


def main():
    serial_port = "COM7"  # Replace with your actual serial port
    output_file = "raw_eeg_data2.csv"
    streaming_duration = 10000000  # Stream indefinetely
    interval = 10  # Process data every 10 seconds

    # Initialize and start the EEGProcessor
    processor = EEGProcessor(serial_port, output_file, streaming_duration, interval)
    processor.initialize_board()
    processor.start_processing()


if __name__ == "__main__":
    BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG)
    main()
