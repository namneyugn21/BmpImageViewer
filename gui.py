"""
The GUI module for the BMP image display application.
This module contains functions to create the GUI elements and handle user interactions.
Methods:
  - browse_file(file_input, message_box, display_container, image_container, customise_container): Opens a file dialog to select a BMP file and displays the metadata and image on the GUI.
  - display_meta_data(filepath, display_container): Displays metadata of the BMP file on the GUI.
  - apply_transformations(image_container): Applies the current brightness & scale transformations to the original pixel data, then displays the result in image_container.
  - display_pixel_data(pixel_data, image_container): Renders a 2D list of (r,g,b) tuples as a tk.PhotoImage and shows it in image_container.
  - on_brightness_slider(value, image_container): Function is called whenever the brightness slider changes. Updates global brightness and re-applies transformations.
  - on_scale_slider(value, image_container): Function is called whenever the scale slider changes. Updates global scale and re-applies transformations.
  - setup_ui(root): Sets up the user interface for the BMP image display application.
"""

import tkinter as tk
import tkinter.filedialog
import threading
from accessors import get_file_size, get_image_width, get_image_height, get_bpp, is_bmp
from image_parser import read_bmp_pixel
from brightness import apply_brightness
from scaling import scale_pixels

# define global variables
original_pixels = None                 # store the original pixel data
current_brightness = 100               # slider 0-100
current_scale = 100                    # slider 0-100
filepath_loaded = None                 # store the path for reference
r_var = None    
g_var = None
b_var = None

def browse_file(file_input, message_box, display_container, image_container):
  """
  Opens a file dialog to select a BMP file and displays the metadata and image on the GUI.
  """
  global original_pixels, filepath_loaded
  message_box.config(text="")

  path = tk.filedialog.askopenfilename(title="Select a BMP file")
  if not path:
    return

  # validate BMP
  if not is_bmp(path):
    message_box.config(text="Please upload a BMP file.", fg="red")
    return
  else:
    message_box.config(text="Successfully uploaded BMP file.", fg="green")

  # update entry field
  file_input.delete(0, tk.END)
  file_input.insert(0, path)
  filepath_loaded = path

  # clear previous data
  for widget in display_container.winfo_children():
    widget.destroy()
  for widget in image_container.winfo_children():
    widget.destroy()

  # display metadata
  display_meta_data(path, display_container)

  # read the original pixel data once, store globally
  input_pixels = read_bmp_pixel(path)
  if input_pixels is None:
    message_box.config(text="Failed to read BMP pixel data.", fg="red")
    return
  
  # check if image is bigger than the display area
  h = len(input_pixels)
  w = len(input_pixels[0])
  MAX_W = 500
  MAX_H = 300

  if w > MAX_W or h > MAX_H:
    from scaling import scale_pixels
    factor_w = MAX_W / w
    factor_h = MAX_H / h
    factor = min(factor_w, factor_h)
    scale_percent = int(factor * 100)
    input_pixels = scale_pixels(input_pixels, scale_percent)

  original_pixels = input_pixels

  # display the original image
  apply_transformations(image_container)

def display_meta_data(filepath, display_container):
  """
  Displays metadata of the BMP file on the GUI.
  """
  file_size = tk.Label(
    display_container,
    text=f"File Size: {get_file_size(filepath)} bytes",
    font=("Arial", 12), anchor="center"
  )
  file_size.grid(row=0, column=0, sticky="ew", padx=10, pady=2)

  width_label = tk.Label(
    display_container,
    text=f"Image Width: {get_image_width(filepath)} pixels",
    font=("Arial", 12), anchor="center"
  )
  width_label.grid(row=1, column=0, sticky="ew", padx=10, pady=2)

  height_label = tk.Label(
    display_container,
    text=f"Image Height: {get_image_height(filepath)} pixels",
    font=("Arial", 12), anchor="center"
  )
  height_label.grid(row=2, column=0, sticky="ew", padx=10, pady=2)

  bpp_label = tk.Label(
    display_container,
    text=f"Bits Per Pixel: {get_bpp(filepath)} bits",
    font=("Arial", 12), anchor="center"
  )
  bpp_label.grid(row=3, column=0, sticky="ew", padx=10, pady=(2, 20))

def apply_transformations(image_container):
  """
  Applies the current brightness & scale transformations to the original pixel data,
  Then displays the result in image_container by calling display_pixel_data.
  """
  global original_pixels, current_brightness, current_scale, r_enabled, g_enabled, b_enabled

  if original_pixels is None: # no image loaded, return
    return

  # apply brightness by calling the function from brightness.py
  bright_data = apply_brightness(original_pixels, current_brightness)

  # apply scaling by calling the function from scaling.py
  final_data = scale_pixels(bright_data, current_scale)

  # read the current RGB toggle values
  r_enabled = r_var.get()
  g_enabled = g_var.get()
  b_enabled = b_var.get()

  # apply RGB toggle
  for y in range(len(final_data)):
    for x in range(len(final_data[y])):
      r, g, b = final_data[y][x]
      if not r_enabled:
        r = 0
      if not g_enabled:
        g = 0
      if not b_enabled:
        b = 0
      final_data[y][x] = (r, g, b)

  # render on the GUI
  display_pixel_data(final_data, image_container)

def display_pixel_data(pixel_data, image_container):
  """
  Displayu the pixel data as an image in the image_container.
  """
  # clear the container
  for widget in image_container.winfo_children():
    widget.destroy()

  if not pixel_data or len(pixel_data) == 0:
    return

  height = len(pixel_data)
  width = len(pixel_data[0])

  img = tk.PhotoImage(width=width, height=height)
  for y in range(height):
    row_data = "{" + " ".join(
      f"#{r:02x}{g:02x}{b:02x}" for (r, g, b) in pixel_data[y]
    ) + "}"
    img.put(row_data, (0, y))

  lbl = tk.Label(image_container, image=img)
  lbl.image = img
  container_width = image_container.winfo_width()
  container_height = image_container.winfo_height()
  offset_x = (container_width - width) // 2
  offset_y = (container_height - height) // 2
  lbl.place(x=offset_x, y=offset_y)

def on_brightness_slider(value, image_container):
  """
  Function is called whenever the brightness slider changes.
  Updates global brightness and re-applies transformations.
  """
  global current_brightness
  current_brightness = int(value)
  apply_transformations(image_container)

def on_scale_slider(value, image_container):
  """
  Function is called whenever the scale slider changes.
  Updates global scale and re-applies transformations.
  """
  global current_scale
  current_scale = int(value)
  apply_transformations(image_container)

def setup_ui(root):
  """
  Sets up the user interface for the BMP image display application.
  """
  global r_var, g_var, b_var

  # create the channel toggles 
  r_var = tk.BooleanVar(value=True, master=root)
  g_var = tk.BooleanVar(value=True, master=root)
  b_var = tk.BooleanVar(value=True, master=root)
  
  root.title("BMP Image Display")

  header = tk.Label(root, text="BMP Image Display", font=("Arial", 18))
  header.grid(row=0, column=0, columnspan=2, pady=(20, 10))

  file_input = tk.Entry(root, width=50)
  file_input.grid(row=1, column=0, padx=(10, 5), pady=10)

  message_box = tk.Label(root, text="Please upload a .bmp file.\nThe program will display metadata & image.")
  message_box.grid(row=2, column=0, columnspan=2, pady=(0, 20))

  upload_button = tk.Button(root, text="Upload", command=lambda: browse_file(file_input, message_box, display_container, image_container))
  upload_button.grid(row=1, column=1, padx=(5, 10), pady=10)

  display_container = tk.Frame(root)
  display_container.grid(row=3, column=0, columnspan=2, sticky="ew")
  display_container.columnconfigure(0, weight=1)

  image_container = tk.Frame(root, width=500, height=300)
  image_container.grid(row=4, column=0, columnspan=2)
  image_container.propagate(False)

  customise_container = tk.Frame(root)
  customise_container.grid(row=5, column=0, columnspan=2)

  # brightness
  brightness_text = tk.Label(customise_container, text="Brightness", font=("Arial", 12))
  brightness_text.grid(row=0, column=0, columnspan=2, pady=(15, 0))
  brightness_slider = tk.Scale(
    customise_container,
    from_=0,
    to=100,
    orient="horizontal",
    length=150,
    command=lambda val: on_brightness_slider(val, image_container)
  )
  brightness_slider.set(100)
  brightness_slider.grid(row=1, column=0, columnspan=2, padx=10)

  # scaling
  scaling_text = tk.Label(customise_container, text="Scaling", font=("Arial", 12))
  scaling_text.grid(row=2, column=0, columnspan=2, pady=(15, 0))
  scaling_slider = tk.Scale(
    customise_container,
    from_=0,
    to=100,
    orient="horizontal",
    length=150,
    command=lambda val: on_scale_slider(val, image_container)
  )
  scaling_slider.set(100)
  scaling_slider.grid(row=3, column=0, columnspan=2, padx=10)

  # rgb toggle
  rgb_text = tk.Label(customise_container, text="RGB Toggle", font=("Arial", 12))
  rgb_text.grid(row=4, column=0, columnspan=2, pady=(15, 0))
  toggle_container = tk.Frame(customise_container)
  toggle_container.grid(row=5, column=0, columnspan=2, pady=(0, 30))
  # create toggle buttons for RGB                        
  red_btn = tk.Checkbutton(
    toggle_container, 
    text="Red",
    variable=r_var,
    command=lambda: apply_transformations(image_container)
  )
  red_btn.grid(row=0, column=0, padx=(0, 10), pady=(15, 0))

  green_btn = tk.Checkbutton(
    toggle_container, 
    text="Green",
    variable=g_var,
    command=lambda: apply_transformations(image_container)
  )
  green_btn.grid(row=0, column=1, pady=(15, 0))

  blue_btn = tk.Checkbutton(
    toggle_container, 
    text="Blue", 
    variable=b_var,
    command=lambda:  apply_transformations(image_container)
  )
  blue_btn.grid(row=0, column=2, padx=(10, 0), pady=(15, 0))