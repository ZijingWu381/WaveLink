import time
import numpy as np
import pandas as pd
from brainflow.board_shim import BoardShim, BrainFlowInputParams, LogLevels, BoardIds
from brainflow.data_filter import DataFilter
import logging


def initialize_board(serial_port):
    """
    Initialize the BrainFlow board with the given serial port and configure channels with specific gains.
    """
    BoardShim.enable_board_logger()
    params = BrainFlowInputParams()
    params.serial_port = serial_port
    board = BoardShim(BoardIds.NEUROPAWN_KNIGHT_BOARD, params)

    print("Preparing session...")
    board.prepare_session()
    print("Starting data stream...")
    board.start_stream(450000)

    print(board.is_prepared())

    return board


def save_data_to_csv(data, filename="data_output.csv"):
    """
    Save the BrainFlow data to a CSV file using pandas.
    """
    # Transpose the data to match the expected format (channels as columns)
    df = pd.DataFrame(np.transpose(data))

    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


def main():
    serial_port = "COM3"  # Replace with your actual serial port
    try:
        # Initialize the board and configure channels
        board = initialize_board(serial_port)
        board_id = board.get_board_id()
        chans = board.get_exg_channels(board_id)
        
        time.sleep(2)

        # Configure specific channels if needed
        board.config_board("chon_5_12")  # Example: Configure channel 5 with gain 12
        time.sleep(2)
        board.config_board("chon_8_12")  # Example: Configure channel 8 with gain 12
        time.sleep(5)

        for _ in range(10):  # Stream for 10 iterations (10 seconds)
            # Get the latest data from the board
            data = np.array(board.get_current_board_data(500))
            df = pd.DataFrame(data).transpose()
            print(df)

            # Save the data to a CSV file
            save_data_to_csv(data, "data_output.csv")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Ensure resources are released
        print("Releasing session...")
        if board.is_prepared():
            board.release_session()


if __name__ == "__main__":
    BoardShim.enable_dev_board_logger()
    logging.basicConfig(level=logging.DEBUG)
    main()