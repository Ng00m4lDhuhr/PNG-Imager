import os
import struct
from sys import argv, stderr

def read_pixel_count(file_path):
    with open(file_path, 'rb') as file:
        # Seek to the beginning of the file
        file.seek(8)  # PNG files start with an 8-byte signature
        # Initialize pixel count
        pixel_count = 0
        while True:
            try:
                # Read chunk length
                chunk_length_bytes = file.read(4)
                if not chunk_length_bytes:
                    break  # Reached end of file

                # Convert chunk length bytes to integer
                chunk_length = struct.unpack('!I', chunk_length_bytes)[0]

                # Skip chunk type and CRC
                file.seek(chunk_length + 4, os.SEEK_CUR)

                # Increment pixel count based on IHDR chunk
                if chunk_length == 13:
                    # Each pixel consists of 3 bytes (RGB)
                    width_bytes = file.read(4)
                    height_bytes = file.read(4)
                    width = struct.unpack('!I', width_bytes)[0]
                    height = struct.unpack('!I', height_bytes)[0]
                    pixel_count = width * height
                    break  # Found IHDR chunk, no need to continue reading
            except struct.error:
                break  # Error occurred while reading file
    return pixel_count

def get_pixel_count(file_path):
    with open(file_path, 'rb') as file:
        # Seek to the beginning of the file
        file.seek(8)  # PNG files start with an 8-byte signature

        # Skip IHDR chunk length (4 bytes) and type (4 bytes)
        file.seek(8, os.SEEK_CUR)

        # Read width and height from IHDR chunk
        width_bytes = file.read(4)
        height_bytes = file.read(4)
        width = struct.unpack('!I', width_bytes)[0]
        height = struct.unpack('!I', height_bytes)[0]

        # Calculate pixel count
        pixel_count = width * height

        # Calculate number of bytes per pixel (3 bytes for RGB)
        bytes_per_pixel = 3

        # Skip to pixel data
        file.seek(4, os.SEEK_CUR)  # Skip CRC

        # Initialize pixel count
        pixel_count_manual = 0

        # Iterate through pixel data
        while True:
            try:
                # Read each pixel (3 bytes for RGB)
                pixel_data = file.read(bytes_per_pixel)
                if not pixel_data:
                    break  # Reached end of file
                pixel_count_manual += 1
            except struct.error:
                break  # Error occurred while reading file

    return pixel_count_manual


def main():
    try: file_path = argv[1]
    except IndexError :
        print("SYNTAX : python3 PixelImager.py [imageFile]",file=stderr)
        exit(1)
    # Iterate through files in folder
    pixel_count = get_pixel_count(file_path)
    print(f"File: {file_path}, Pixel Count: {pixel_count}")

if __name__ == "__main__":
    main()
