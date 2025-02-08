"""
This module contains functions for adjusting the brightness of an image.
Methods:
  - rgb_to_yuv(r, g, b): Converts an RGB color to YUV color space.
  - yuv_to_rgb(y, u, v): Converts a YUV color to RGB color space.
  - adjust_brightness(y, factor): Adjusts the brightness of the Y component by a factor.
  - apply_brightness(pixel_data, brightness_percent): Applies the brightness adjustment to the entire pixel array.
"""

def rgb_to_yuv(r, g, b):
  y = 0.299 * r + 0.587 * g + 0.114 * b
  u = -0.299 * r - 0.587 * g + 0.886 * b
  v = 0.701 * r - 0.587 * g - 0.114 * b
  return (y, u, v)

def yuv_to_rgb(y, u, v):
  r = y + v
  g = y - 0.194 * u - 0.509 * v
  b = y + u

  # Clamp to [0, 255]
  r = int(min(max(r, 0), 255))
  g = int(min(max(g, 0), 255))
  b = int(min(max(b, 0), 255))
  return (r, g, b)

def adjust_brightness(y, factor):
  """
  Multiply the Y component by a brightness factor (0.0 to 1.0),
  Then clamp to [0, 255].
  """
  y *= factor
  return min(max(y, 0), 255)

def apply_brightness(pixel_data, brightness_percent):
  """
  Applies the brightness adjustment to the entire pixel array.
  """
  factor = brightness_percent / 100.0
  new_pixel_data = []

  for row in pixel_data:
    new_row = []
    for (r, g, b) in row:
      y, u, v = rgb_to_yuv(r, g, b)
      y = adjust_brightness(y, factor)
      r2, g2, b2 = yuv_to_rgb(y, u, v)
      new_row.append((r2, g2, b2))
    new_pixel_data.append(new_row)

  return new_pixel_data
