import os
import shutil
from PIL import Image, ImageSequence
from alive_progress import alive_bar
from termcolor import colored

# Increase decompression limit
Image.MAX_IMAGE_PIXELS = None

def compress_image(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img.save(output_path, quality=quality, optimize=True)

def convert_png_to_webp(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        img.save(output_path, 'webp', quality=quality, optimize=True)

def convert_png_to_jpg(input_path, output_path, quality=85):
    with Image.open(input_path) as img:
        rgb_img = img.convert('RGB')
        rgb_img.save(output_path, quality=quality, optimize=True)

def compress_gif(input_path, output_path):
    with Image.open(input_path) as img:
        frames = [frame.copy() for frame in ImageSequence.Iterator(img)]
        frames[0].save(output_path, save_all=True, append_images=frames[1:], optimize=True)

def get_file_size(file_path):
    return os.path.getsize(file_path)

def has_transparency(img):
    if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
        return True
    return False

def compress_images_in_directory(directory, quality=85):
    supported_formats = ('.jpg', '.jpeg', '.png', '.webp', '.jfif', '.gif')

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
    gif_compressed_count = 0

    with alive_bar(len(image_files), title='Compressing Images') as bar:
        for root, file in image_files:
            input_path = os.path.join(root, file)
            file_ext = os.path.splitext(file)[1].lower()

            if file_ext == '.png':
                with Image.open(input_path) as img:
                    if has_transparency(img):
                        temp_output_path = os.path.join(root, f"temp_{os.path.splitext(file)[0]}.webp")
                    else:
                        temp_output_path = os.path.join(root, f"temp_{os.path.splitext(file)[0]}.jpg")
                png_converted_count += 1
            elif file_ext == '.gif':
                temp_output_path = os.path.join(root, f"temp_{file}")
                gif_compressed_count += 1
            else:
                temp_output_path = os.path.join(root, f"temp_{file}")

            try:
                original_size = get_file_size(input_path)
                total_original_size += original_size

                if file_ext == '.png':
                    with Image.open(input_path) as img:
                        if has_transparency(img):
                            convert_png_to_webp(input_path, temp_output_path, quality)
                        else:
                            convert_png_to_jpg(input_path, temp_output_path, quality)
                elif file_ext == '.gif':
                    compress_gif(input_path, temp_output_path)
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
        print(colored(f"Total GIF files compressed: {gif_compressed_count}", "red"))

if __name__ == "__main__":
    directory = r"F:\\\Walls"
    #directory = r"C:\\Users\\ZnK\\Downloads\\pn"
    quality = 85
    compress_images_in_directory(directory, quality)
