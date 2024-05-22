import os
import shutil
from PIL import Image
from alive_progress import alive_bar
from termcolor import colored

def compress_image(input_path, output_path, quality=75):
    with Image.open(input_path) as img:
        img.save(output_path, quality=quality, optimize=True)

def convert_png_to_jpg(input_path, output_path, quality=75):
    with Image.open(input_path) as img:
        rgb_img = img.convert('RGB')
        rgb_img.save(output_path, quality=quality, optimize=True)

def get_file_size(file_path):
    return os.path.getsize(file_path)

def compress_images_in_directory(directory, quality=75):
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp', '.jfif')

    pre_directory = os.path.join(directory, 'pre')
    os.makedirs(pre_directory, exist_ok=True)

    image_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(supported_formats):
                image_files.append((root, file))

    total_original_size = 0
    total_compressed_size = 0
    png_converted_count = 0

    with alive_bar(len(image_files), title='Compressing Images') as bar:
        for root, file in image_files:
            input_path = os.path.join(root, file)
            if file.lower().endswith('.png'):
                temp_output_path = os.path.join(root, f"temp_{os.path.splitext(file)[0]}.jpg")
                png_converted_count += 1
            else:
                temp_output_path = os.path.join(root, f"temp_{file}")

            try:
                original_size = get_file_size(input_path)
                total_original_size += original_size

                if file.lower().endswith('.png'):
                    convert_png_to_jpg(input_path, temp_output_path, quality)
                else:
                    compress_image(input_path, temp_output_path, quality)

                compressed_size = get_file_size(temp_output_path)
                total_compressed_size += compressed_size

                shutil.move(input_path, os.path.join(pre_directory, file))
                shutil.move(temp_output_path, input_path)

                bar()
            except Exception as e:
                print(f"Failed to compress {input_path}: {e}")
                bar()

    if total_original_size > 0:
        total_reduction = ((total_original_size - total_compressed_size) / total_original_size) * 100
        total_original_size_mb = total_original_size / (1024 * 1024)
        total_compressed_size_mb = total_compressed_size / (1024 * 1024)

        print(colored(f"Total original size: {total_original_size_mb:.2f} MB", "red"))
        print(colored(f"Total compressed size: {total_compressed_size_mb:.2f} MB", "red"))
        print(colored(f"Total reduction: {total_reduction:.2f}%", "red"))
        print(colored(f"Total PNG files converted: {png_converted_count}", "red"))

if __name__ == "__main__":
#    directory = r"F:\\\Walls"
    directory = r"C:\\Users\\XXX\\Downloadss" 
    quality = 75
    compress_images_in_directory(directory, quality)
