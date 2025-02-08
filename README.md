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
