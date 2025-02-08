"""
This module provides a function to scale a 2D list of pixel data.
Methods:
  - nearest_neighbor_scale(pixel_data, scale_factor): Scale the given pixel_data by scale_factor (float).
  - scale_pixels(pixel_data, scale_percent): Wraps nearest_neighbor_scale in a simpler signature.
"""

def nearest_neighbor_scale(pixel_data, scale_factor):
  """
  Scale the given pixel_data by scale_factor (float).
  pixel_data: 2D list of (r, g, b).
  Scale_factor: e.g. 0.75 means 75% of original size.
  Returns a new 2D list with scaled dimensions.
  """
  original_height = len(pixel_data)
  if original_height == 0:
    return pixel_data  

  original_width = len(pixel_data[0])
  if original_width == 0:
    return pixel_data

  new_width = max(1, int(original_width * scale_factor))
  new_height = max(1, int(original_height * scale_factor))

  new_pixel_data = []
  for y in range(new_height):
    # map to nearest original row
    original_y = int(y / scale_factor)
    row = []
    for x in range(new_width):
      # map to nearest original column
      original_x = int(x / scale_factor)
      row.append(pixel_data[original_y][original_x])
    new_pixel_data.append(row)

  return new_pixel_data

def scale_pixels(pixel_data, scale_percent):
  # if scale_percent = 0, don't display anything
  if scale_percent <= 0:
    return []

  factor = scale_percent / 100.0
  return nearest_neighbor_scale(pixel_data, factor)
