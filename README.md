# BMP Image Processor

A Python-based GUI application for displaying, modifying, and analyzing BMP images. The application allows users to adjust brightness and scale images using nearest-neighbor interpolation, all within a user-friendly Tkinter interface.

## Features
- Upload BMP images and display them.
- View image metadata, including file size, dimensions, and bits per pixel.
- Adjust brightness using YUV color space.
- Scale images from 0% to 100% using nearest-neighbor interpolation.
- Multi-threaded processing for a smooth user experience.

## Installation & Setup

### Install Dependencies
Ensure you have Python 3.7 or higher installed. Install required dependencies:
```sh
pip install tk
```sh

### Clone the Repository
```sh
git clone https://github.com/your-username/bmp-processor.git
cd bmp-processor
```sh

### Run the Application
```sh
python main.py
```sh

## Usage Guide

### Uploading an Image
Click "Upload" and select a BMP file. The image will be displayed along with its metadata.

### Adjusting Brightness
Move the Brightness slider (0-100%) to adjust the image brightness. The changes are applied using multi-threading to avoid UI freezing.

### Scaling the Image
Adjust the Scaling slider (0-100%) to resize the image. Uses nearest-neighbor interpolation for rescaling.

## Project Structure
```
bmp-processor/
│── accessors.py         # Get image metadata (width, height, bpp, file size)
│── brightness.py        # Adjust brightness using YUV color space
│── scaling.py           # Implement nearest-neighbor interpolation for scaling
│── image_parser.py      # Read BMP pixel data
│── gui.py               # Main GUI for displaying image & metadata
│── display.py           # Image rendering functions
│── main.py              # Entry point to start the application
│── README.md            # Project documentation
```

## Technologies Used
- Python
- Tkinter (GUI framework)
- Nearest-Neighbor Interpolation (for image scaling)
- YUV Color Space (for brightness adjustment)

## Contact
- Email: vhn1@sfu.ca
- GitHub: namneyugn21