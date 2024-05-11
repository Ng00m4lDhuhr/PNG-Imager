from PIL import Image
import io
from sys import argv, stderr

def hex_to_image(hex_values:bytes, width:int, height:int) -> object:
    data = hex_values
    img = Image.new('L', (width, height))
    img.putdata([b for b in data])
    return img

def read_binary_file(file_path:str):
    with open(file_path, 'rb') as file:
        binary_data = file.read()
    return binary_data

def save_image(img:object, filename:str) -> None:
    img.save(filename)

def display_image(img:object):
    img.show()

if __name__ == '__main__':
    try:
        if '-h' in argv: raise IndexError
        hex_values = read_binary_file(argv[1])
        try:
            width = int(argv[2])
            height = int(argv[3])
        except ValueError: raise IndexError
        img = hex_to_image(hex_values, width, height)
        display_image(img)
        save_image(img, f"{width}x{height}.PNG")

    except IndexError:
        print("SYNTAX: [binary file path] [width] [height]" ,file=stderr)
