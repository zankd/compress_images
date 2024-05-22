Image Compression Script

This Python script compresses image files within a specified directory. It supports various image formats, including PNG, JPEG, WebP, and GIF, optimizing them to reduce file sizes while maintaining acceptable quality. Additionally, it handles PNG files with transparency by converting them to WebP format, and it can optimize GIFs.

Setup and Initialization:

Imports necessary libraries (os, shutil, PIL for image processing, alive_progress for progress bar, and termcolor for colored console output).

Creates a subdirectory (pre) to store the original images before compression.

For each image file:

 - Determines the appropriate compression or conversion method based on the file extension and properties (e.g., transparency for PNG).
 - Compresses or converts the image.
 - Moves the original image to the pre subdirectory and replaces it with the compressed version.
 - Updates progress and logs the results.
 - Calculates and prints the total size reduction achieved.

Install Dependencies:

pip install pillow alive-progress termcolor

Run the Script.

 - Modify the directory variable in the script to point to the directory containing your images.
 - Set the desired quality level (an integer between 0 and 100, where 100 is the best quality).

Notes
The script creates a pre subdirectory within the specified directory to store the original images before compression.
PNG files with transparency are converted to WebP format to preserve transparency.
GIF files are optimized but not converted to another format.
