import os
from PIL import Image

def compress_image(image_path, output_path, quality=85):
    """Compresses the image and saves it to the output folder."""
    with Image.open(image_path) as img:
        # Convert to RGB if the image is PNG (JPEG doesn't support transparency)
        img = img.convert("RGB")
        # Save the image as JPEG with the given quality (for compression)
        img.save(output_path, "JPEG", optimize=True, quality=quality)

def compress_images_in_folder(folder_name, quality=85):
    """Compress all images in the 'images' folder inside each NFT folder."""
    images_folder = os.path.join(folder_name, "images")
    
    if os.path.exists(images_folder):
        for image_file in os.listdir(images_folder):
            if image_file.endswith((".png", ".jpg", ".jpeg")):
                image_path = os.path.join(images_folder, image_file)
                output_path = image_path  # Overwrite the original image

                # Compress the image
                compress_image(image_path, output_path, quality)
                print(f"Compressed: {image_path}")
    else:
        print(f"No 'images' folder found in {folder_name}")

def compress_all_nft_folders(base_folder, num_folders=100, quality=85):
    """Iterates over each NFT folder and compresses images inside."""
    for folder_id in range(1, num_folders + 1):
        folder_name = os.path.join(base_folder, f"fight4hope-{folder_id}")
        compress_images_in_folder(folder_name, quality)

if __name__ == "__main__":
    # Base folder containing the NFT folders (fight4hope-1, fight4hope-2, etc.)
    base_nft_folder = "./"  # Assuming folders are in the current directory
    
    # Compress images in all NFT folders (from fight4hope-1 to fight4hope-100)
    compress_all_nft_folders(base_nft_folder, num_folders=100, quality=85)
