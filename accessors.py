'''
This file contains functions to check if a file is a BMP file and to display BMP file meta data.
Methods:
  - is_bmp(filepath): Checks if the file is a BMP file by reading the first 2 bytes of the file.
  - get_file_size(filepath): Reads the file size from the BMP file header.
  - get_image_width(filepath): Reads the image width from the BMP file header.
  - get_image_height(filepath): Reads the image height from the BMP file header.
  - get_bpp(filepath): Reads the bits per pixel (bpp) from the BMP file header.
  - get_pixel_data_offset(filepath): Reads the pixel data offset from the BMP file header.
'''

# define function to check if file is BMP
def is_bmp(filepath):
  with open(filepath, "rb") as f: # open file in binary code
    header = f.read(2) # read first 2 bytes
    return header == b"BM" # check if first 2 bytes are "BM", b"BM" is a byte string
  
# define function to display BMP file meta data
def get_file_size(filepath):
  with open(filepath, "rb") as f:
    f.seek(2) # skip first 2 bytes
    file_size = int.from_bytes(f.read(4), "little") # read next 4 bytes as little-endian integer
    return file_size
  
def get_image_width(filepath):
  with open(filepath, "rb") as f:
    f.seek(18) # skip first 18 bytes
    image_width = int.from_bytes(f.read(4), "little") # read next 4 bytes as little-endian integer
    return image_width 
  
def get_image_height(filepath):
  with open(filepath, "rb") as f:
    f.seek(22) # skip first 22 bytes
    image_height = int.from_bytes(f.read(4), "little") # read next 4 bytes as little-endian integer
    return image_height
  
def get_bpp(filepath):
  with open(filepath, "rb") as f:
    f.seek(28) # skip first 28 bytes
    bpp = int.from_bytes(f.read(2), "little") # read next 2 bytes as little-endian integer
    return bpp
  
def get_pixel_data_offset(filepath): # get pixel data offset to start reading pixel data
  with open(filepath, "rb") as f:
    f.seek(10) # skip first 10 bytes
    pixel_data_offset = int.from_bytes(f.read(4), "little") # read next 4 bytes as little-endian integer
    return pixel_data_offset