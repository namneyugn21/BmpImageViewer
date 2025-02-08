'''
This file contains functions to read pixel data from BMP image files, and it will parse the pixel data based on the bits per pixel (bpp) value.
Methods:
  - read_bmp_pixel(filepath): Reads the pixel data from a BMP image file and returns a 2D list of pixel values in RGB format.
'''

from accessors import get_image_width, get_image_height, get_bpp, get_pixel_data_offset

# define function to read bmp pixel data
def read_bmp_pixel(filepath):
  width = get_image_width(filepath)
  height = get_image_height(filepath)
  bpp = get_bpp(filepath)
  pixel_data_offset = get_pixel_data_offset(filepath)

  with open(filepath, "rb") as f:
    f.seek(pixel_data_offset) # skip to pixel data offset

    row_padding = (4 - (width * (bpp // 8) % 4)) % 4 # ensure row size is a multiple of 4
    pixel_data = []

    # read color table (for 1, 4, 8 bpp)
    color_table = []
    # this part converts the color table to RGB format
    if bpp in [1, 4, 8]:
      f.seek(54) # skip to color table
      num_colors = 2 ** bpp # number of colors in palette
      for _ in range(num_colors):
        b, g, r, _ = f.read(4) # read 4 bytes for each color (RGB values are stored backwards i.e. BGR.)
        color_table.append((r, g, b)) # store color in RGB format

    f.seek(pixel_data_offset) # skip to pixel data offset

    for row in range(height):
      row_pixels = []

      if bpp == 24: 
        for col in range(width):
          blue = int.from_bytes(f.read(1), "little")
          green = int.from_bytes(f.read(1), "little")
          red = int.from_bytes(f.read(1), "little")
          row_pixels.append((red, green, blue))
      
      elif bpp == 8: # one byte per pixel
        for col in range(width): # go through each pixel in the row
          color_index = int.from_bytes(f.read(1), "little") # read 1 byte as little-endian integer
          row_pixels.append(color_table[color_index]) # get color from color table using color index defined above

      elif bpp == 4: # half byte per pixel, left 4 bits is color index for pixel 1, right 4 bits is color index for pixel 2
        for col in range(0, width, 2): # go through 2 pixels at a time in the row
          byte = int.from_bytes(f.read(1), "little") # read 1 byte as little-endian integer
          # get color index for left pixel and right pixel
          left_pixel = (byte >> 4) & 0b00001111 # get left 4 bits
          right_pixel = byte & 0b00001111
          row_pixels.append(color_table[left_pixel]) # get color from color table using color index defined above
          row_pixels.append(color_table[right_pixel])
      
      elif bpp == 1: # one bit per pixel
        for col in range(0, width, 8): # go through 8 pixels at a time in the row
          byte = int.from_bytes(f.read(1), "little") # read 1 byte as little-endian integer
          # get color index for each pixel
          for i in range(8):
            color_index = (byte >> (7 - i)) & 0b00000001
            row_pixels.append(color_table[color_index])

      f.read(row_padding) # skip row padding
      pixel_data.insert(0, row_pixels) # insert row pixels at the beginning of the list to display image correctly

    return pixel_data