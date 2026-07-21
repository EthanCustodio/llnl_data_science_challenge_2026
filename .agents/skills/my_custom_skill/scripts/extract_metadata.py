import numpy as np
import os
import sys


def extract_metadata(file_path):
    """
    Loads a .npy file and prints basic metadata to the terminal:
    shape, data type, and the maximum and minimum values.

    Args:
        file_path (str): Path to the .npy file to inspect.
    """
    if not os.path.exists(file_path):
        print(f"Error: File not found at {file_path}")
        return

    print(f"Loading data from {file_path}...")
    data = np.load(file_path)

    print("=" * 40)
    print(f"File:      {file_path}")
    print(f"Shape:     {data.shape}")
    print(f"Data type: {data.dtype}")
    if data.size > 0:
        print(f"Min value: {data.min()}")
        print(f"Max value: {data.max()}")
    else:
        print("Min value: N/A (empty array)")
        print("Max value: N/A (empty array)")
    print("=" * 40)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python extract_metadata.py <path_to_file.npy>")
        sys.exit(1)

    extract_metadata(sys.argv[1])
