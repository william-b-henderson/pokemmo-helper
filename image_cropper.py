import os

from PIL import Image


def clip_transparent(image_path, output_path):
    # Open the image using Pillow
    img = Image.open(image_path)

    # Convert the image to RGBA if it's not in that mode already
    img = img.convert("RGBA")

    # Get the non-transparent region
    non_transparent_region = Image.new('RGBA', img.size, (255, 255, 255, 0))
    non_transparent_region.paste(img, (0, 0), img)

    bbox = non_transparent_region.getbbox()
    # Find the bounding box for the non-transparent region

    if bbox:
        # Crop the image to the non-transparent region
        img = img.crop(bbox)
        img.save(output_path)
        print(f"Image cropped and saved to {output_path}")
    else:
        print("No non-transparent regions found in the image.")


def process_images_in_folder(folder_path):
    if not os.path.exists(folder_path):
        print(f"Folder '{folder_path}' does not exist.")
        return

    output_folder = os.path.abspath('sprites2')
    os.makedirs(output_folder, exist_ok=True)

    for filename in os.listdir(folder_path):
        if filename.endswith(".png"):
            input_image_path = os.path.join(folder_path, filename)
            output_image_path = os.path.join(
                output_folder, filename)

            clip_transparent(input_image_path, output_image_path)


sprites_folder_path = "sprites"

process_images_in_folder(sprites_folder_path)
